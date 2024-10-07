# Base Python Application
# Image tag: scraper-base

FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN set -eux; \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY src/scrap ./scrap
