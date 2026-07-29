import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = "you@example.com"       
MY_PASSWORD = "your_app_passwords" 
MY_LAT = 30.309065   
MY_LONG = 71.943004  

TEST_MODE = False 

def send_email():
    """Sends the 'Look Up' notification email."""
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look Up\n\nThe ISS is above you in the sky."
        )


def is_iss_overhead():
    """Returns True if the ISS is within 5 degrees of your location."""
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    return False


def is_night():
    """Returns True if it is currently night time at your location."""
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True
    return False


if TEST_MODE:
    print("TEST MODE: sending one test email now, ignoring ISS/night conditions...")
    send_email()
    print("Test email sent! Check your inbox. Set TEST_MODE = False to run the real notifier.")
else:
    print("ISS Overhead Notifier started. Checking every 60 seconds...")

    while True:
        time.sleep(60)
        if is_iss_overhead() and is_night():
            print("ISS is overhead and it's night — sending email!")
            send_email()
        else:
            print("Not time yet. Checking again in 60 seconds...")