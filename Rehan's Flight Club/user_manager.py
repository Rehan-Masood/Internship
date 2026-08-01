import requests
from credentials import SHEETY_USERS_ENDPOINT, SHEETY_USERNAME, SHEETY_PASSWORD


class UserManager:
    """Handles new sign-ups and reading the subscriber list for the flight club."""

    def __init__(self):
        self._auth = (SHEETY_USERNAME, SHEETY_PASSWORD)

    def get_all_users(self):
        """Returns every subscribed user as a list of dicts (firstName, lastName, email)."""
        response = requests.get(url=SHEETY_USERS_ENDPOINT, auth=self._auth)
        response.raise_for_status()
        return response.json()["users"]

    def add_user(self, first_name, last_name, email):
        """Adds a new subscriber row to the Google Sheet via Sheety."""
        new_user = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
            }
        }
        response = requests.post(url=SHEETY_USERS_ENDPOINT, json=new_user, auth=self._auth)
        response.raise_for_status()
        return response.json()
