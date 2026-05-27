# Deployment Guide

## Local Production Smoke Run
```powershell
pip install -r requirements.txt
python manage.py collectstatic --noinput
gunicorn backend.config.wsgi:application
```

## Docker
```powershell
docker compose up --build
```

## Render or Railway
1. Create PostgreSQL database.
2. Set `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, and `DATABASE_URL`.
3. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
4. Start command: `gunicorn backend.config.wsgi:application --bind 0.0.0.0:$PORT`

## AWS
Use ECS/Fargate or EC2 with Docker Compose. Put Nginx or an Application Load Balancer in front, terminate TLS, and persist `media/` in S3 for production.

