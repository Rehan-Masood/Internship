import os
import re
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)

# ============================================================
# CORS
# ============================================================

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5500"
).rstrip("/")

ALLOWED_ORIGINS = {
    FRONTEND_URL,
    "https://rehanmasood.dev",
    "https://www.rehanmasood.dev",
}

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": list(ALLOWED_ORIGINS)
        }
    }
)

# ============================================================
# SMTP CONFIGURATION
# ============================================================

SMTP_SERVER = os.getenv(
    "SMTP_SERVER",
    "smtp.gmail.com"
)

SMTP_PORT = int(
    os.getenv(
        "SMTP_PORT",
        "587"
    )
)

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

CONTACT_RECEIVER_EMAIL = os.getenv(
    "CONTACT_RECEIVER_EMAIL",
    "jrehan590@gmail.com"
)


# ============================================================
# HELPERS
# ============================================================

def clean(value, max_length):
    """
    Convert input to a safe trimmed string and limit its length.
    """
    return str(value or "").strip()[:max_length]


def valid_email(email):
    """
    Basic email validation.
    """
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email))


# ============================================================
# FRONTEND
# ============================================================

@app.get("/")
def home():
    """
    Serve the portfolio homepage.
    """
    return send_from_directory(
        BASE_DIR,
        "index.html"
    )


# ============================================================
# PROFILE IMAGE
# ============================================================

@app.get("/profile.png")
def profile_image():
    """
    Serve the portfolio profile image.
    """
    return send_from_directory(
        BASE_DIR,
        "profile.png"
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health():
    return jsonify({
        "service": "portfolio-contact-backend",
        "status": "healthy"
    })


# ============================================================
# CONTACT API
# ============================================================

@app.post("/api/contact")
def contact():

    # --------------------------------------------------------
    # Request validation
    # --------------------------------------------------------

    if not request.is_json:
        return jsonify(
            success=False,
            message="Request must contain JSON data."
        ), 400

    data = request.get_json(
        silent=True
    ) or {}

    name = clean(
        data.get("name"),
        100
    )

    email = clean(
        data.get("email"),
        254
    )

    subject = clean(
        data.get("subject"),
        200
    )

    message = clean(
        data.get("message"),
        5000
    )

    # --------------------------------------------------------
    # Required fields
    # --------------------------------------------------------

    if not all([
        name,
        email,
        subject,
        message
    ]):
        return jsonify(
            success=False,
            message="All fields are required."
        ), 400

    # --------------------------------------------------------
    # Email validation
    # --------------------------------------------------------

    if not valid_email(email):
        return jsonify(
            success=False,
            message="Please enter a valid email address."
        ), 400

    # --------------------------------------------------------
    # SMTP configuration check
    # --------------------------------------------------------

    if not SMTP_EMAIL or not SMTP_PASSWORD:

        app.logger.error(
            "SMTP_EMAIL or SMTP_PASSWORD is missing."
        )

        return jsonify(
            success=False,
            message="Email service is not configured."
        ), 500

    # --------------------------------------------------------
    # Create email
    # --------------------------------------------------------

    msg = EmailMessage()

    msg["From"] = SMTP_EMAIL
    msg["To"] = CONTACT_RECEIVER_EMAIL
    msg["Reply-To"] = email
    msg["Subject"] = f"Portfolio Contact: {subject}"

    msg.set_content(
        f"""New message received from your portfolio.

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

This message was sent from the portfolio contact form.
"""
    )

    # --------------------------------------------------------
    # Send email
    # --------------------------------------------------------

    try:

        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=20
        ) as server:

            server.ehlo()

            server.starttls()

            server.ehlo()

            server.login(
                SMTP_EMAIL,
                SMTP_PASSWORD
            )

            server.send_message(msg)

        return jsonify(
            success=True,
            message="Your message has been sent successfully!"
        ), 200

    except smtplib.SMTPAuthenticationError:

        app.logger.exception(
            "SMTP authentication failed."
        )

        return jsonify(
            success=False,
            message="Email service authentication failed."
        ), 500

    except smtplib.SMTPException:

        app.logger.exception(
            "SMTP error while sending portfolio message."
        )

        return jsonify(
            success=False,
            message="Unable to send your message right now."
        ), 500

    except Exception:

        app.logger.exception(
            "Unexpected error while sending portfolio message."
        )

        return jsonify(
            success=False,
            message="An unexpected server error occurred."
        ), 500


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )