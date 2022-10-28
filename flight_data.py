import requests
import os

TEQUILA_LOC = "https://api.tequila.kiwi.com/locations/query"
TEQUILA_API = os.environ["TEQUILA_API_KEY"]


# This class is responsible for structuring the flight data.
class FlightData:
    def __init__(self, destination, price, id_code, IATA="",):
        self.destination = destination.title()
        self.price = price
        self.to_update = False
        self.id_code = id_code
        self.IATA = self.get_IATA() if IATA == '' else IATA

    def get_IATA(self):
        self.to_update = True
        header = {"apikey": TEQUILA_API, 'accept': 'application/json'}
        params = {"term": self.destination, "location_types": "city"}
        response = requests.get(url=TEQUILA_LOC, headers=header, params=params)
        if response.status_code == 200:
            return response.json()["locations"][0]["code"]
        else:
            print(f"ERROR, IATA code for {self.destination} not found.")
            return ""

