import smtplib
from credentials import MY_EMAIL, MY_PASSWORD

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


class NotificationManager:
    """Sends an email alert to every subscribed user whenever a cheap flight deal is found."""

    def send_flight_email(self, flight, recipient_emails):
        """Sends a formatted email describing a flight deal to a list of recipient email addresses."""
        subject = f"Low price alert! Only £{flight.price} to fly to {flight.destination_city}"

        message = (
            f"Low price alert!\n\n"
            f"Only £{flight.price} to fly from {flight.origin_airport} "
            f"to {flight.destination_city} ({flight.destination_airport}).\n\n"
            f"Departure: {flight.out_date}\n"
        )
        if flight.return_date:
            message += f"Return: {flight.return_date}\n"
        message += f"Stops: {flight.stops}\n"

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)

            for recipient in recipient_emails:
                try:
                    connection.sendmail(
                        from_addr=MY_EMAIL,
                        to_addrs=recipient,
                        msg=f"Subject:{subject}\n\n{message}".encode("utf-8"),
                    )
                    print(f"Email sent to {recipient} for deal to {flight.destination_city}.")
                except smtplib.SMTPException as error:
                    print(f"Failed to email {recipient}: {error}")