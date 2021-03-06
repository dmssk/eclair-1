from __future__ import annotations

import http
import json

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import BaseFormView

from shop.models import CartProduct


class Cart(BaseFormView):
    def get(self, request: WSGIRequest, *args, **kwargs):
        if not request.session.session_key:
            return JsonResponse(data=[], safe=False)

        cart_product = CartProduct.objects.filter(
            session_id=request.session.session_key
        ).all()

        products = [{"title": p.product_id, "amount": p.amount} for p in cart_product]
        return JsonResponse(data=products, safe=False)

    def put(self, request: WSGIRequest, *args, **kwargs):
        data = json.loads(self.request.body)
        article = data["article"]
        amount = data["amount"]

        if not request.session.session_key:
            request.session.create()

        cart_product, is_new = CartProduct.objects.get_or_create(
            product_id=article, session_id=request.session.session_key
        )
        if not is_new:
            if cart_product.amount + amount <= 0:
                cart_product.delete()
            else:
                # Todo: check that new amount won't exceed stock or some limit
                cart_product.amount = F("amount") + amount
                cart_product.save()

        return HttpResponse(status=http.HTTPStatus.CREATED)
