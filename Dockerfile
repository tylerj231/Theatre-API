FROM python:3.11-slim
LABEL maintainer="jacktyler2391@gmail.com"

ENV PYTHONBUFFERED 1

WORKDIR /core

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
