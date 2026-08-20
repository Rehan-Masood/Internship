import time
from datetime import datetime
import requests

USERNAME = "rehan-demo-2026"
TOKEN = "your_own_Token"
GRAPH_ID = "cycling-demo"

PIXELA_ENDPOINT = "https://pixe.la/v1/users"
GRAPH_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"
PIXEL_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}"

headers = {"X-USER-TOKEN": TOKEN}


def make_request_with_retry(
    url, method="POST", headers=None, json_data=None, max_retries=5
):
    """Handles Pixela's free tier ~25% random rejections by automatically retrying."""
    for attempt in range(1, max_retries + 1):
        try:
            if method.upper() == "POST":
                response = requests.post(url, json=json_data, headers=headers)
            elif method.upper() == "PUT":
                response = requests.put(url, json=json_data, headers=headers)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                response = requests.get(url, headers=headers)

            res_json = response.json()

            # Check if Pixela randomly rejected the request
            if res_json.get("isRejected") is True:
                print(
                    f"Pixela free-tier rate rejection. Retrying ({attempt}/{max_retries})..."
                )
                time.sleep(1)
                continue

            return response.text

        except Exception as e:
            print(f"Network error: {e}. Retrying ({attempt}/{max_retries})...")
            time.sleep(1)

    return '{"message": "Request failed after maximum retries.", "isSuccess": false}'


def create_account():
    """Creates your Pixela user account. Only needs to be run once, ever."""
    user_params = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    result = make_request_with_retry(
        url=PIXELA_ENDPOINT, method="POST", json_data=user_params
    )
    print(result)


def create_graph():
    """Creates a new graph on your account. Only needs to be run once per graph."""
    graph_config = {
        "id": GRAPH_ID,
        "name": "Cycling Graph",
        "unit": "Km",
        "type": "float",
        "color": "ajisai",
    }
    result = make_request_with_retry(
        url=GRAPH_ENDPOINT,
        method="POST",
        json_data=graph_config,
        headers=headers,
    )
    print(result)


def log_today():
    """Logs today's habit entry (e.g. how many km you cycled today)."""
    today = datetime.now().strftime("%Y%m%d")
    quantity = input("How many kilometers did you cycle today? ").strip()

    pixel_data = {
        "date": today,
        "quantity": quantity,
    }
    result = make_request_with_retry(
        url=PIXEL_ENDPOINT, method="POST", json_data=pixel_data, headers=headers
    )
    print(result)


def update_today():
    """Updates today's already-logged entry with a new value."""
    today = datetime.now().strftime("%Y%m%d")
    new_quantity = input("Enter the corrected value for today: ").strip()

    new_pixel_data = {
        "quantity": new_quantity,
    }
    result = make_request_with_retry(
        url=f"{PIXEL_ENDPOINT}/{today}",
        method="PUT",
        json_data=new_pixel_data,
        headers=headers,
    )
    print(result)


def delete_today():
    """Deletes today's entry entirely."""
    today = datetime.now().strftime("%Y%m%d")
    result = make_request_with_retry(
        url=f"{PIXEL_ENDPOINT}/{today}", method="DELETE", headers=headers
    )
    print(result)


if __name__ == "__main__":
    while True:
        print("\nWhat would you like to do?")
        print("1. Create Pixela account (do this once)")
        print("2. Create graph (do this once per graph)")
        print("3. Log today's entry")
        print("4. Update today's entry")
        print("5. Delete today's entry")
        print("6. Quit")

        choice = input("Enter a number (1-6): ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            create_graph()
        elif choice == "3":
            log_today()
        elif choice == "4":
            update_today()
        elif choice == "5":
            delete_today()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Please enter a valid number between 1 and 6.")
