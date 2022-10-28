import os
from flight_data import FlightData
from pprint import pprint

import requests

SH_TOKEN = os.environ["SH_TOKEN"]
SH_EP = os.environ["SH_EP"]
SH_EP_U = os.environ["SH_EP_U"]


# This class is responsible for talking to the Google Sheet.
class DataManager:

    def __init__(self):
        self.sh_headers = {"Authorization": SH_TOKEN, "Content-Type": "application/json"}
        response = requests.get(url=SH_EP, headers=self.sh_headers)
        data = response.json()["prices"]
        self.flight_data = [FlightData(destination=info['city'], price=info['lowestPrice'],
                                       id_code=info['id'], IATA=info['iataCode']) for info in data]
        self.update_destination()

    def add_destination(self, destination, price):
        add = True
        for data in self.flight_data:
            if data.destination == destination:
                add = False
        if add is True:
            new_flight = FlightData(destination=destination, price=price, id_code=self.flight_data[-1].id_code + 1, IATA='')
            row = {
                "price": {
                    "city": new_flight.destination,
                    "iataCode": new_flight.IATA,
                    "lowestPrice": new_flight.price
                }
            }
            response = requests.post(url=f"{SH_EP}", headers=self.sh_headers, json=row)
            response.raise_for_status()
            self.flight_data.append(new_flight)

    def update_destination(self):
        for data in self.flight_data:
            if data.to_update is True:
                row = {
                    "price": {
                        "city": data.destination,
                        "iataCode": data.IATA,
                        "lowestPrice": data.price
                    }
                }
                response = requests.put(url=f"{SH_EP}/{data.id_code}", headers=self.sh_headers, json=row)
                response.raise_for_status()
                data.to_update = False

    def get_flight_data(self):
        return self.flight_data

    def get_users_email(self):
        response = requests.get(url=SH_EP_U, headers=self.sh_headers)
        data = response.json()["users"]
        return [user["email"] for user in data]

