import requests
import datetime as dt
import os


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
    TEQUILA_API_KEY = os.getenv("TEQUILA_API_KEY")
    tequila_password = os.getenv("TEQUILA_PASSWORD")
    HOME = "VIE"

    def get_city_code(self, city):
        headers = {"apikey": self.TEQUILA_API_KEY}

        params = {
            "term": city,
            "location-types": "city",
            "active-only": "true",
            "limit": "1",
        }

        response = requests.get(
            url=f"{self.TEQUILA_ENDPOINT}/locations/query",
            params=params,
            headers=headers,
        )

        return response.json()["locations"][0]["code"]

    def get_flight(self, city_code, max_stopovers=0):
        today = dt.datetime.now()
        today_date = today.strftime("%d/%m/%Y")
        six_months = dt.timedelta(days=180)
        date_six_months_from_now = (today + six_months).strftime("%d/%m/%Y")

        headers = {"apikey": self.TEQUILA_API_KEY}

        params = {
            "fly_from": f"city:{self.HOME}",
            "fly_to": f"city:{city_code}",
            "date_from": today_date,
            "date_to": date_six_months_from_now,
            "nights_in_dst_from": 2,
            "nights_in_dst_to": 14,
            "flight_type": "round",
            "one_for_city": 1,
            "max_sector_stopovers": max_stopovers,
            "curr": "EUR",
            "limit": 1,
        }
        response = requests.get(
            url=f"{self.TEQUILA_ENDPOINT}/v2/search", params=params, headers=headers
        )

        try:
            flight_data = response.json()["data"][0]
        except IndexError:
            params["max_sector_stopovers"] = 1
            response = requests.get(
                url=f"{self.TEQUILA_ENDPOINT}/v2/search", params=params, headers=headers
            )
            try:
                flight_data = response.json()["data"][0]
                flight_info = {
                "from": flight_data["cityFrom"],
                "from_airport": flight_data["cityCodeFrom"],
                "to": flight_data["cityTo"],
                "to_airport": flight_data["cityCodeTo"],
                "departure_date": flight_data["route"][0]["local_departure"].split("T")[
                    0
                ],
                "return_date": flight_data["route"][2]["local_departure"].split("T")[0],
                "price": flight_data["price"],
                "nights_in_destination": flight_data["nightsInDest"],
                "stopovers": params["max_sector_stopovers"],
                "stopover_city": flight_data["route"][0]["cityTo"]
            }
            except IndexError:
                print("nothing found")
                return None
        
        else:
            flight_info = {
                "from": flight_data["cityFrom"],
                "from_airport": flight_data["cityCodeFrom"],
                "to": flight_data["cityTo"],
                "to_airport": flight_data["cityCodeTo"],
                "departure_date": flight_data["route"][0]["local_departure"].split("T")[
                    0
                ],
                "return_date": flight_data["route"][1]["local_departure"].split("T")[0],
                "price": flight_data["price"],
                "nights_in_destination": flight_data["nightsInDest"],
                "stopovers": params["max_sector_stopovers"],
            }

        finally:
            return flight_info