from __future__ import annotations


import enum
import logging
from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import urljoin

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class ClientError(Exception):
    pass


class PaymentType(enum.Enum):
    CASH = 34113529
    CARD = 34113523


@dataclass
class Order:
    order_id: str
    total_amount: int
    payment_type: PaymentType
    content: str
    address: str


class Client:
    SITE_PIPELINE_ID = 3428449
    ROBOT_ID = 0

    def __init__(self, options):
        self._url = options["url"]
        self._secret_key = options["secret_key"]
        self._integration_id = options["integration_id"]
        self._auth_code = options["auth_code"]
        self._http_client = requests.Session()
        self._access_token = ""
        self._refresh_token = ""
        self._redirect_url = options["redirect_url"]

    def init_token(self):
        try:
            self._obtain_access_token_local()
        except FileNotFoundError:
            self._obtain_access_token_external()

    def _obtain_access_token_external(self):
        """https://www.amocrm.ru/developers/content/oauth/step-by-step#get_access_token"""
        url = urljoin(self._url, "/oauth2/access_token")
        resp = self._http_client.post(
            url,
            data={
                "client_id": self._integration_id,
                "client_secret": self._secret_key,
                "grant_type": "authorization_code",
                "code": self._auth_code,
                "redirect_uri": self._redirect_url,
            },
        )
        if not resp.ok:
            raise ClientError(resp.text)

        data = resp.json()
        self._access_token = data["access_token"]
        self._refresh_token = data["refresh_token"]
        self._write_tokens(self._access_token, self._refresh_token)
        return

    def _refresh_access_token(self):
        """https://www.amocrm.ru/developers/content/oauth/step-by-step#easy_auth"""
        url = urljoin(self._url, "/oauth2/access_token")
        resp = self._http_client.post(
            url,
            data={
                "client_id": self._integration_id,
                "client_secret": self._secret_key,
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
                "redirect_uri": "https://dmssk.github.io/",
            },
        )
        if not resp.ok:
            raise ClientError(resp.text)

        data = resp.json()
        self._access_token = data["access_token"]
        self._refresh_token = data["refresh_token"]
        self._write_tokens(self._access_token, self._refresh_token)
        return

    def _obtain_access_token_local(self):
        with open(settings.BASE_DIR / ".amocrm_tokens", "r") as fh:
            self._access_token = fh.readline()
            self._refresh_token = fh.readline()

    def _write_tokens(self, access_token: str, refresh_token: str):
        with open(settings.BASE_DIR / ".amocrm_tokens", "w") as fh:
            fh.write(f"{access_token}\n{refresh_token}")

    def _send_get(self, endpoint: str) -> dict[Any, Any]:
        url = urljoin(self._url, endpoint)

        for _ in range(2):
            resp = self._http_client.get(
                url, headers={"Authorization": f"Bearer {self._access_token}"}
            )
            if not resp.ok:
                # refresh token and retry
                self._refresh_access_token()
            else:
                break

        if not resp.ok:
            raise ClientError(resp.text)

        data = resp.json()
        return data

    def _send_post(self, endpoint: str, data: Optional[Any]) -> dict[Any, Any]:
        url = urljoin(self._url, endpoint)

        for _ in range(2):
            resp = self._http_client.post(
                url,
                headers={"Authorization": f"Bearer {self._access_token}"},
                json=data,
            )
            if not resp.ok:
                # refresh token and retry
                self._refresh_access_token()
            else:
                break

        if not resp.ok:
            raise ClientError(resp.text)

        data = resp.json()
        return data

    def get_leads(self):
        """https://www.amocrm.ru/developers/content/crm_platform/leads-api"""
        return self._send_get("api/v4/leads")

    def get_lead(self, id_: int):
        """https://www.amocrm.ru/developers/content/crm_platform/leads-api"""
        return self._send_get(f"api/v4/leads/{id_}")

    def create_lead(self, contact_id: int, order: Order):
        """https://www.amocrm.ru/developers/content/crm_platform/leads-api"""
        product_field_id = 608539
        address_field_id = 608543

        data = self._send_post(
            "api/v4/leads",
            [
                {
                    "name": order.order_id,
                    "price": order.total_amount,
                    "pipeline_id": self.SITE_PIPELINE_ID,
                    "created_by": self.ROBOT_ID,
                    "status_id": order.payment_type,
                    # https://www.amocrm.ru/developers/content/crm_platform/custom-fields#cf-fill-examples
                    "custom_fields_values": [
                        {
                            "field_id": product_field_id,
                            "values": [{"value": order.content}],
                        },
                        {
                            "field_id": address_field_id,
                            "values": [{"value": order.address}],
                        },
                    ],
                    "_embedded": {
                        "contacts": [
                            {
                                "id": contact_id,
                            }
                        ]
                    },
                }
            ],
        )
        return data

    def list_contacts(self):
        """https://www.amocrm.ru/developers/content/crm_platform/contacts-api"""
        return self._send_get("api/v4/contacts/")

    def get_contact(self, id_: int):
        """https://www.amocrm.ru/developers/content/crm_platform/contacts-api"""
        return self._send_get(f"api/v4/contacts/{id_}")

    def create_contact(self, name: str, phone: str) -> str:
        """https://www.amocrm.ru/developers/content/crm_platform/contacts-api"""
        name_id = 430823
        email_id = 430825

        data = self._send_post(
            "api/v4/contacts",
            data=[
                {
                    "first_name": name,
                    "created_by": self.ROBOT_ID,
                    "custom_fields_values": [
                        {
                            "field_id": name_id,
                            "values": [{"value": phone, "enum_id": 806581}],
                        }
                    ],
                }
            ],
        )

        contact = data["_embedded"]["contacts"][0]
        return contact["id"]


client = Client(
    {
        "url": settings.AMOCRM_URL,
        "integration_id": settings.AMOCRM_INTEGRATION_ID,
        "secret_key": settings.AMOCRM_SECRET_KEY,
        "auth_code": settings.AMOCRM_AUTH_CODE,
        "redirect_url": settings.AMOCRM_REDIRECT_URL,
    }
)

try:
    client.init_token()
except Exception as ex:
    logger.error("Failed to init amocrm client. Order creation will not work: %s", ex)
