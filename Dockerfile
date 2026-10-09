FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DB_PATH=/data/downloads.db

WORKDIR /opt/torbox-monitor

RUN addgroup --system app && \
    adduser --system --ingroup app --home /nonexistent --no-create-home app && \
    mkdir -p /data && \
    chown app:app /data

COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt

COPY --chown=app:app app ./app

USER app

VOLUME ["/data"]

CMD ["python", "-u", "app/main.py"]
