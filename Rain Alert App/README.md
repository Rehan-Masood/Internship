# Rain Alert App

Rain Alert App is a small Python script that checks the OpenWeatherMap forecast for your location and sends a WhatsApp alert through Twilio when rain is expected.

## How It Works

1. The script requests the next forecast from OpenWeatherMap.
2. It checks the weather condition codes for rain.
3. If rain is likely, it sends a WhatsApp message with Twilio.

## Features

- Forecast-based rain detection
- WhatsApp notification via Twilio
- Simple single-file Python project

## Requirements

- Python 3.9 or newer
- Internet access
- OpenWeatherMap API key
- Twilio account with WhatsApp enabled

## Installation

Clone or copy the project files, then install the Python dependencies:

```bash
pip install requests twilio
```

## Configuration

Update the values in `main.py` with your own credentials and location:

- `OWM_API_KEY` - OpenWeatherMap API key
- `MY_LAT` and `MY_LONG` - your latitude and longitude
- `TWILIO_SID` - your Twilio account SID
- `TWILIO_AUTH_TOKEN` - your Twilio auth token
- `TWILIO_WHATSAPP_NUMBER` - Twilio WhatsApp sender number
- `MY_WHATSAPP_NUMBER` - your WhatsApp number

For safety, it is better to keep API keys and phone numbers in environment variables instead of hard-coding them in the source file.

## Usage

Run the script with:

```bash
python main.py
```

If rain is expected in the forecast window, the script sends a WhatsApp alert. Otherwise, it prints that no message was sent.

## Test Mode

Set `TEST_MODE = True` in `main.py` to send a test WhatsApp message without checking the forecast.

## Notes

- The forecast check uses the next 12 hours of data.
- Weather condition codes below `700` are treated as rain-related conditions.
- The current `main.py` contains a duplicated block at the end; it does not change the intended behavior, but it should be cleaned up later.

## Screenshot

The repository includes sample images that appear to show the project or its output:

- `Message-Received for testing.jpg`
- `Real-Time Working.jpg`
