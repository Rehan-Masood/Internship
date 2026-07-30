import requests
from twilio.rest import Client

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
OWM_API_KEY = "9e22b99883a564b89b80d63d9a8c35c1"   

MY_LAT = 30.309065  
MY_LONG = 71.943004  


TWILIO_SID = "your_twilio_account_sid_here"        
TWILIO_AUTH_TOKEN = "your_twilio_auth_token_here"  
TWILIO_WHATSAPP_NUMBER = "whatsapp:+143456789"    
MY_WHATSAPP_NUMBER = "whatsapp:+92324596433"       

TEST_MODE = False  


def is_rain_coming():
    """Checks the next 12 hours of forecast data and returns True if rain is expected."""
    parameters = {
        "lat": MY_LAT,
        "lon": MY_LONG,
        "appid": OWM_API_KEY,
        "cnt": 4, 
    }

    response = requests.get(OWM_ENDPOINT, params=parameters)
    response.raise_for_status()
    weather_data = response.json()

    will_rain = False
    for hour_data in weather_data["list"]:
        condition_code = hour_data["weather"][0]["id"]
        if int(condition_code) < 700:
            will_rain = True

    return will_rain


def send_rain_whatsapp():
    """Sends a WhatsApp message via Twilio warning about rain."""
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella.",
        from_=TWILIO_WHATSAPP_NUMBER,
        to=MY_WHATSAPP_NUMBER,
    )
    print(f"Message sent. Status: {message.status}")


if TEST_MODE:
    print("TEST MODE: sending one test WhatsApp message now, ignoring real forecast...")
    send_rain_whatsapp()
    print("Test message sent! Check your WhatsApp. Set TEST_MODE = False to run the real check.")
elif is_rain_coming():
    print("Rain expected — sending WhatsApp alert...")
    send_rain_whatsapp()
else:
    print("No rain expected in the next 12 hours. No message sent.")

def send_rain_whatsapp():
    """Sends a WhatsApp message via Twilio warning about rain."""
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella.",
        from_=TWILIO_WHATSAPP_NUMBER,
        to=MY_WHATSAPP_NUMBER,
    )
    print(f"Message sent. Status: {message.status}")


if TEST_MODE:
    print("TEST MODE: sending one test WhatsApp message now, ignoring real forecast...")
    send_rain_whatsapp()
    print("Test message sent! Check your WhatsApp. Set TEST_MODE = False to run the real check.")
elif is_rain_coming():
    print("Rain expected — sending WhatsApp alert...")
    send_rain_whatsapp()
else:
    print("No rain expected in the next 12 hours. No message sent.")
