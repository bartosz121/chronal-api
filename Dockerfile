FROM python:3.10.8-slim-buster

ENV IS_DEV=True
ENV ALLOWED_ORIGINS=[*]

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --no-cache-dir --upgrade /usr/src/app