import requests
from credentials import SHEETY_PRICES_ENDPOINT, SHEETY_USERNAME, SHEETY_PASSWORD


class DataManager:
    """Reads and updates the destinations Google Sheet (prices tab) via the Sheety API."""

    def __init__(self):
        self.destination_data = {}
        self._auth = (SHEETY_USERNAME, SHEETY_PASSWORD)

    def get_destination_data(self):
        """Fetches every row from the Google Sheet."""
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self._auth)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        """Writes the IATA code back to the sheet for every row currently in self.destination_data."""
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                auth=self._auth,
            )
            response.raise_for_status()