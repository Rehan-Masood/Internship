import requests
from datetime import datetime

USERNAME = "rehan-demo-2026"   # <-- CHANGE THIS: lowercase letters, numbers, hyphens only
TOKEN = "RehanDemoToken2026"  # <-- CHANGE THIS: your own secret token (letters/numbers, no spaces)
GRAPH_ID = "cycling-demo"       # <-- CHANGE THIS: id for this specific graph

PIXELA_ENDPOINT = "https://pixe.la/v1/users"
GRAPH_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"
PIXEL_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}"

headers = {
    "X-USER-TOKEN": TOKEN
}


def create_account():
    """Creates your Pixela user account. Only needs to be run once, ever."""
    user_params = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    response = requests.post(url=PIXELA_ENDPOINT, json=user_params)
    print(response.text)


def create_graph():
    """Creates a new graph on your account. Only needs to be run once per graph."""
    graph_config = {
        "id": GRAPH_ID,
        "name": "Cycling Graph",
        "unit": "Km",
        "type": "float",
        "color": "ajisai",
    }
    response = requests.post(url=GRAPH_ENDPOINT, json=graph_config, headers=headers)
    print(response.text)


def log_today():
    """Logs today's habit entry (e.g. how many km you cycled today)."""
    today = datetime.now().strftime("%Y%m%d")
    quantity = input("How many kilometers did you cycle today? ")

    pixel_data = {
        "date": today,
        "quantity": quantity,
    }
    response = requests.post(url=PIXEL_ENDPOINT, json=pixel_data, headers=headers)
    print(response.text)


def update_today():
    """Updates today's already-logged entry with a new value."""
    today = datetime.now().strftime("%Y%m%d")
    new_quantity = input("Enter the corrected value for today: ")

    new_pixel_data = {
        "quantity": new_quantity,
    }
    response = requests.put(url=f"{PIXEL_ENDPOINT}/{today}", json=new_pixel_data, headers=headers)
    print(response.text)


def delete_today():
    """Deletes today's entry entirely."""
    today = datetime.now().strftime("%Y%m%d")
    response = requests.delete(url=f"{PIXEL_ENDPOINT}/{today}", headers=headers)
    print(response.text)


while True:
    print("\nWhat would you like to do?")
    print("1. Create Pixela account (do this once)")
    print("2. Create graph (do this once per graph)")
    print("3. Log today's entry")
    print("4. Update today's entry")
    print("5. Delete today's entry")
    print("6. Quit")

    choice = input("Enter a number (1-6): ")

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
        break
    else:
        print("Please enter a number between 1 and 6.")