FROM python:3.12-alpine3.19

COPY requirements.txt /temp/requirements.txt
COPY constr_fin /constr_fin
WORKDIR /constr_fin
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev gettext

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password constr-user

USER constr-user