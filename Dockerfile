FROM python:3.9-slim-buster
WORKDIR app

RUN pip install -U pip && pip install pipenv

COPY Pipfile* .
RUN pipenv install --system

COPY . .

ENV DJANGO_SETTINGS_MODULE eclair.settings
CMD python manage.py runserver 0.0.0.0:8000