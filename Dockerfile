FROM python:3.12-slim

# WeasyPrint system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpango-1.0-0 libpangoft2-1.0-0 libcairo2 libgdk-pixbuf-2.0-0 \
        libffi-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# collectstatic at build time. Placeholders satisfy prod.py validation;
# Render's runtime env vars override them at container start.
ENV DJANGO_SETTINGS_MODULE=config.settings.prod \
    SECRET_KEY=build-only-collectstatic \
    ALLOWED_HOSTS=build
RUN python manage.py collectstatic --noinput

COPY start.sh .
RUN chmod +x start.sh

EXPOSE 8000
CMD ["./start.sh"]
