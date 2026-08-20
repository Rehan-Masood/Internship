from datetime import datetime
import requests

WEIGHT_KG = 62
WEIGHT_LBS = WEIGHT_KG * 2.20462

# 1. Enter your API Ninjas Key
NINJA_API_KEY = "your_ninja_api_key"
EXERCISE_ENDPOINT = "https://api.api-ninjas.com/v1/caloriesburned"

# 2. Sheety Endpoint
SHEET_ENDPOINT = (
    "https://api.sheety.co/3f473a58591f924c5cecd6607fea337e/myWorkouts/sheet1"
)


def get_exercise_data(activity_text, duration_min=60):
    headers = {"X-Api-Key": NINJA_API_KEY}
    parameters = {
        "activity": activity_text.strip(),
        "weight": int(round(WEIGHT_LBS)),
        "duration": duration_min,
    }

    response = requests.get(
        EXERCISE_ENDPOINT, params=parameters, headers=headers
    )
    if response.status_code != 200:
        print(f"API Ninjas Error: {response.text}")
        response.raise_for_status()

    return response.json()


def log_to_sheet(exercises):
    today_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")

    exercise = exercises[0]

    sheet_inputs = {
        "sheet1": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise.get("name", "Unknown").title(),
            "duration": exercise.get("duration_minutes", 60),
            "calories": exercise.get("total_calories", 0),
        }
    }

    # No auth parameter needed when Auth is set to None in Sheety
    sheet_response = requests.post(SHEET_ENDPOINT, json=sheet_inputs)
    print(f"\nSheety response:\n{sheet_response.text}\n")


if __name__ == "__main__":
    exercise_input = input(
        "Which exercise did you do? (e.g., running, cycling): "
    ).strip()
    duration_input = input("For how many minutes? (default 60): ").strip()

    duration = int(duration_input) if duration_input.isdigit() else 60

    if exercise_input:
        exercises = get_exercise_data(exercise_input, duration)
        if exercises:
            log_to_sheet(exercises)
            print("Done! Check your Google Sheet.")
        else:
            print("No matching exercise found.")
