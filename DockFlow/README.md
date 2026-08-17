# DockFlow

**DockFlow — Containerized Flask Deployment & CI/CD Platform**

A premium dark/colorful Flask DevOps dashboard with real backend data,
Docker discovery, GitHub Actions integration, application metrics,
logs, health checks and responsive real-time polling.

## Important design rule

The provided UI reference is a visual model only. It is not the source of
dashboard data. DockFlow never hardcodes screenshot metrics or pretends
that integrations are connected.

If Docker is unavailable, the UI says so. If GitHub is not configured, it
says so. Deployment records are only written after a configured deployment
trigger is accepted.

## Features

- Flask application factory and blueprints
- SQLite persistence for metrics, logs, activities and deployments
- Real request count and response-time collection
- Live CPU, memory and disk monitoring with psutil
- Docker SDK integration with graceful unavailable state
- GitHub Actions status and workflow dispatch
- Deployment webhook integration
- `/health` endpoint
- Dark premium responsive dashboard
- AJAX polling without full-page reloads
- Dockerfile + Docker Compose
- GitHub Actions CI and Docker smoke test
- pytest suite
- Safe environment variables

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
python run.py
```

Open `http://localhost:5000`.

## Docker

```bash
docker compose up --build
```

Open `http://localhost:5000`.

For live host-container discovery on Linux, you may mount
`/var/run/docker.sock` in `docker-compose.yml`. Treat Docker socket access
as privileged and only enable it when you understand the security impact.

## GitHub Actions

Set these environment variables for the dashboard's GitHub API integration:

- `GITHUB_TOKEN`
- `GITHUB_OWNER`
- `GITHUB_REPO`
- `GITHUB_WORKFLOW`
- `GITHUB_REF`

The token should be a GitHub secret in deployment environments. The
workflow itself runs tests, compiles Python and builds/smoke-tests Docker.

## Deployment

The repository includes the CI/CD structure needed for Render/AWS. Provider
credentials and deployment commands are intentionally not hardcoded. Add
the provider-specific deployment step and secrets for your chosen platform.

## API

- `GET /health`
- `GET /api/dashboard`
- `GET /api/health`
- `GET /api/metrics`
- `GET /api/containers`
- `GET /api/ci-status`
- `GET /api/deployments`
- `GET /api/logs`
- `GET /api/monitoring`
- `GET /api/services`

## Testing

```bash
pytest -q
```

## Production

Use Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 --workers 2 --threads 4 run:app
```

Set a strong `SECRET_KEY` and `FLASK_ENV=production`.
CI/CD pipeline verification test.
