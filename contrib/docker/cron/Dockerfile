FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN set -eux; \
    apt-get update; \
    apt-get install -y cron

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

COPY contrib/docker/cron /cron
RUN set -eux; \
    chmod 0700 /cron/*; \
    crontab /cron/jobs

CMD ["/cron/start-cron.sh"]
