import requests
from datetime import datetime

WEIGHT_KG = 62
WEIGHT_LBS = WEIGHT_KG * 2.20462  

NINJA_API_KEY = "your_api_ninja_key"  
EXERCISE_ENDPOINT = "https://api.api-ninjas.com/v1/caloriesburned"

SHEET_ENDPOINT = "https://api.sheety.co/3f473a58591f924c5cecd6607fea337e/myWorkouts/sheet1"           
SHEETY_USERNAME = "your_username"        
SHEETY_PASSWORD = "your_password"  


def get_exercise_data(activity_text, duration_min=60):
    """Sends the exercise name to API Ninjas and returns the parsed exercise list."""
    headers = {
        "X-Api-Key": NINJA_API_KEY,
    }
    parameters = {
        "activity": activity_text,
        "weight": int(round(WEIGHT_LBS)),  
        "duration": duration_min,
    }

    response = requests.get(EXERCISE_ENDPOINT, params=parameters, headers=headers)
    response.raise_for_status()
    result = response.json()
    print(f"\nAPI Ninjas response:\n{result}\n")

    return result


def log_to_sheet(exercises):
    """Logs the top exercise match as a new row in your Google Sheet via Sheety."""
    today_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")

    exercise = exercises[0]

    sheet_inputs = {
        "sheet1": { 
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_minutes"],
            "calories": exercise["total_calories"],
        }
    }

    sheet_response = requests.post(
        SHEET_ENDPOINT,
        json=sheet_inputs,
        auth=(SHEETY_USERNAME, SHEETY_PASSWORD),
    )
    print(f"Sheety response:\n{sheet_response.text}\n")


if __name__ == "__main__":
    exercise_text = input("Which exercise did you do? (e.g., running, cycling): ")
    duration_input = input("For how many minutes? (default 60): ")

    duration = int(duration_input) if duration_input.strip() else 60

    exercises = get_exercise_data(exercise_text, duration)

    if exercises:
        log_to_sheet(exercises)
        print("Done! Check your Google Sheet.")
    else:
        print("No matching exercise found in API Ninjas database.")