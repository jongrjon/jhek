# jhek

Personal, private-first Django site.

- **core** — minimal public homepage.
- **blog** — notes with a four-value visibility enum (`draft` / `private` / `unlisted` / `public`). Managed from Django admin.
- **cv** — structured CV data rendered as HTML or PDF. Login required.

No SPA. No GraphQL. No REST. Server-rendered Django templates only.

## Stack

- Python 3.12
- Django 5.0
- WeasyPrint (PDF rendering) — needs system libs `libpango`, `libcairo`, `libgdk-pixbuf`.
- PostgreSQL in production; SQLite locally by default.
- gunicorn + WhiteNoise in production.

## Local setup (pipenv)

```bash
pipenv install
cp backend/.env.example backend/.env   # then edit SECRET_KEY
pipenv run migrate
pipenv run manage createsuperuser
pipenv run runserver                    # http://127.0.0.1:8000
pipenv run test
```

Available scripts: `manage`, `runserver`, `migrate`, `makemigrations`, `check`, `test`, `shell`.

## URLs

- `/`              homepage
- `/notes/`        notes index (public only)
- `/notes/<slug>/` note detail (respects visibility)
- `/cv/`           CV in default language (login required)
- `/cv/en/` · `/cv/is/`  CV in English / Icelandic
- `/cv/pdf/`       CV as PDF
- `/admin/`        primary editing interface

## Deployment (Render)

The app deploys to [Render](https://render.com) via Docker.

### First-time setup

1. Create a Render account and connect the GitHub repo.
2. Click **New > Blueprint** and select this repo — Render reads `render.yaml` and creates:
   - A **web service** (Docker, free tier)
   - A **PostgreSQL database** (free tier)
3. In the Render dashboard, set the two manual env vars:
   - `ALLOWED_HOSTS` = `your-service-name.onrender.com` (or custom domain)
   - `CSRF_TRUSTED_ORIGINS` = `https://your-service-name.onrender.com`
4. Trigger a manual deploy (or push to `master`).
5. Once deployed, run migrations and create a superuser via the Render **Shell** tab:
   ```
   cd /app && python manage.py migrate
   python manage.py createsuperuser
   ```

### Environment variables

| Variable | Set by | Value |
|---|---|---|
| `DJANGO_SETTINGS_MODULE` | render.yaml | `config.settings.prod` |
| `DATABASE_URL` | Render (auto) | Postgres connection string |
| `SECRET_KEY` | Render (auto) | Generated random value |
| `ALLOWED_HOSTS` | You | Your domain(s), comma-separated |
| `CSRF_TRUSTED_ORIGINS` | You | `https://yourdomain.com` |
| `CV_DEFAULT_LANGUAGE` | render.yaml | `is` |

### Subsequent deploys

Push to `master`. Render auto-builds and deploys. Run `python manage.py migrate` via the Shell tab if migrations were added.

### Static files

Collected at Docker build time via `collectstatic`. Served by WhiteNoise from the Django process. No separate CDN needed.

### PDF generation

WeasyPrint system dependencies (`libpango`, `libcairo`, `libgdk-pixbuf`) are installed in the Docker image. PDF rendering works out of the box.

## CI

GitHub Actions runs on every push and PR to `master`:
- `manage.py check`
- `manage.py test core blog cv`

See `.github/workflows/ci.yml`.

## Settings

- `config/settings/dev.py` — local development (default for `manage.py`)
- `config/settings/prod.py` — production (set via `DJANGO_SETTINGS_MODULE`)
- All secrets from env vars via `django-environ`.

## Project layout

```
backend/
├── config/settings/{base,dev,prod}.py
├── core/           # homepage
├── blog/           # notes, tags, visibility
├── cv/             # CV models + HTML + PDF
├── templates/base.html
├── static/css,images/
├── manage.py
└── requirements.txt
Dockerfile          # production image
render.yaml         # Render service definition
.github/workflows/  # CI
```
