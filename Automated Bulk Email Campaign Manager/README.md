# MailFlow — Automated Bulk Email Campaign Manager

A Flask-based, database-driven email campaign manager inspired by the supplied dashboard reference.

## Features

- CSV contact import
- Contact groups
- Subscription and suppression list
- HTML email templates
- `{{name}}` and `{{email}}` personalization
- SMTP/Gmail sending
- Campaign creation
- Scheduled campaigns
- Hourly rate limiting
- Sent/failed/pending/skipped logging
- Dashboard statistics
- SQLite database
- Bootstrap 5 UI

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py
```

Open http://127.0.0.1:5000

## Gmail

Enable 2-Step Verification and create a Google App Password. Put the App Password in SMTP_PASSWORD if using environment-based configuration.

Alternatively, configure SMTP from the Settings page.

## CSV

```csv
name,email
Ali Raza,ali@example.com
Sara Khan,sara@example.com
```

## Important

Use this application only for recipients who have opted in or where you have a lawful basis to contact them. Keep unsubscribe/suppression handling enabled and respect provider policies and applicable anti-spam/privacy laws.

Never commit `.env`.
