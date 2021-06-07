import requests
from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager


flight_search = FlightSearch()
data_manager = DataManager()
notification_manager = NotificationManager()

sheet_data = data_manager.get_sheet()

# FOR TESTING PURPOSES
# sheet_data = [
#     {"city": "Paris", "iataCode": "PAR", "lowestPrice": "54"},
#     {"city": "Berlin", "iataCode": "BER", "lowestPrice": "42"},
#     {"city": "Tokio", "iataCode": "TYO", "lowestPrice": "485"},
#     {"city": "San Francisco", "iataCode": "SFO", "lowestPrice": "550"},
# ]

user_emails = data_manager.get_all_emails()

for row in sheet_data:
    if not row["iataCode"]:
        row["iataCode"] = flight_search.get_city_code(row["city"])
        data_manager.update_city_code(row["iataCode"], row["id"])

    flight_data = flight_search.get_flight(row["iataCode"])

    # when sheet_data comes from sheety api, remove the int cast
    if flight_data["price"] < int(row["lowestPrice"]):
        print("Found a deal, sending a message")
        notification_manager.send_message(flight_data)
        notification_manager.send_email(flight_data, "milosavljevic.viktor@gmail.com")


print("yes")