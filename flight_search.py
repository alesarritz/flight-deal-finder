import os
import datetime as dt
import requests
import pyshorteners

from_IATA = "CAG"
from_city = "Cagliari"
TEQUILA_SEARCH = "https://api.tequila.kiwi.com/v2/search"
TEQUILA_API = os.environ["TEQUILA_API_KEY"]


class FlightSearch:
    def __init__(self, notificator, flight_data):
        self.notificator = notificator
        self.flight_data = flight_data

    # This class is responsible for talking to the Flight Search API.
    def search(self):
        header = {"apikey": TEQUILA_API, 'accept': 'application/json'}
        tomorrow = (dt.datetime.today() + dt.timedelta(days=1)).strftime("%d/%m/%Y")
        in_6_month = (dt.datetime.today() + dt.timedelta(days=182)).strftime("%d/%m/%Y")

        for data in self.flight_data:
            print(f"Checking flights to {data.destination}..")
            params = {"fly_from": from_IATA, "fly_to": data.IATA, "date_from": tomorrow, "date_to": in_6_month,
                      "flight_type": "round", "nights_in_dst_from": 7, "nights_in_dst_to": 28, "curr": "EUR",
                      "max_stopovers": 0, "price_to": data.price}
            response = requests.get(url=TEQUILA_SEARCH, headers=header, params=params)

            try:
                results = response.json()["data"]
                results = results[0]
            except IndexError:
                params["max_stopovers"] = 2
                response_1_stop = requests.get(url=TEQUILA_SEARCH, headers=header, params=params)
                try:
                    data2 = response_1_stop.json()["data"]
                    data2 = data2[0]
                except IndexError:
                    continue
                else:
                    price = data2["price"]
                    link = pyshorteners.Shortener().tinyurl.short(data2['deep_link'])
                    airport_dest = data2["route"][1]["cityCodeTo"]
                    arrival = data2["route"][0]["local_departure"].split("T")[0]
                    departure = data2["route"][2]["local_departure"].split("T")[0]
                    via_city = data2["route"][0]["cityTo"]

                    self.notificator.add_message(
                        f"Low price alert! Only €{price} to fly from {from_city}-{from_IATA} to "
                        f"{data.destination}-{airport_dest}, from {arrival} to {departure}"
                        f"\nFlight has 1 stop over, via {via_city}.\n"
                        f"Click here to book the flight:\n{link}\n")
            else:
                price = results["price"]
                link = pyshorteners.Shortener().tinyurl.short(results['deep_link'])
                airport_dest = results["route"][0]["cityCodeTo"]
                arrival = results["route"][0]["local_departure"].split("T")[0]
                departure = results["route"][1]["local_departure"].split("T")[0]

                self.notificator.add_message(f"Low price alert! Only €{price} to fly from {from_city}-{from_IATA} to "
                                             f"{data.destination}-{airport_dest}, from {arrival} to {departure}\n"
                                             f"Click here to book the flight:\n{link}\n")
