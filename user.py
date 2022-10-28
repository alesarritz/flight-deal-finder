import requests
import os


class User:
    def __init__(self, name, surname, email):
        self.name = name
        self.surname = surname
        self.email = email

    def add_to_sheet(self):
        sh_headers = {
            "Authorization": os.environ["SH_TOKEN"],
            "Content-Type": "application/json"
        }
        new_row = {
            "user": {
                "firstName": self.name,
                "lastName": self.surname,
                "email": self.email,
            }
        }

        response_sh = requests.post(url=os.environ["SH_EP_U"], headers=sh_headers, json=new_row)
        if response_sh.status_code == 200:
            print("You are in the club!")
