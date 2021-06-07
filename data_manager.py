import requests


class DataManager:
    sheety_API = "https://api.sheety.co/e2a45d65e8fcde798462a03706694a2a/flightDeals"

    def get_sheet(self):
        response = requests.get(f"{self.sheety_API}/prices")
        return response.json()["prices"]

    def get_all_emails(self):
        response = requests.get(f"{self.sheety_API}/users")
        users_data = response.json()["users"]
        return [user["email"] for user in users_data]

    def update_city_code(self, code, id):
        updated_entry = {"price": {"iataCode": code}}

        requests.put(url=f"{self.sheety_API}/{id}", json=updated_entry)

