import requests
import smtplib
from credentials import MY_EMAIL, MY_PASSWORD, SMTP_SERVER, SMTP_PORT

CLUB_NAME = "Rehan's Flight Club"


def send_welcome_email(user_email, first_name):
    """Sends a welcome confirmation email immediately upon sign-up."""
    subject = f"Welcome to {CLUB_NAME}!"
    body = (
        f"Hi {first_name},\n\n"
        f"Thank you for joining {CLUB_NAME}!\n"
        f"You are now set up to receive real-time alerts and manage flight searches.\n\n"
        f"Safe travels,\n"
        f"The {CLUB_NAME} Team"
    )
    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(MY_EMAIL, user_email, message.encode("utf-8"))
        print(f"Welcome email sent to {user_email}.")
    except Exception as error:
        print(f"Failed to send welcome email: {error}")


def run_signup_flow(user_manager):
    """Runs interactive sign-up prompts and registers a new subscriber."""
    print(f"\n==========================================")
    print(f"     Welcome to {CLUB_NAME}     ")
    print(f"==========================================\n")

    first_name = input("Enter your first name: ").strip()
    last_name = input("Enter your last name: ").strip()

    while True:
        email = input("Enter your email: ").strip()
        confirm_email = input("Confirm your email: ").strip()

        if email and email == confirm_email:
            break
        print("Emails do not match. Please try again.\n")

    try:
        user_manager.add_user(first_name, last_name, email)
        print(f"\nSuccess! Welcome to {CLUB_NAME}, {first_name}!")
        send_welcome_email(email, first_name)
        return {"firstName": first_name, "lastName": last_name, "email": email}
    except requests.exceptions.RequestException as error:
        print(f"Sign-up failed: {error}")
        return None