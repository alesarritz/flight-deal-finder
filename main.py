from data_manager import DataManager
from notification_manager import NotificationManager
from flight_search import FlightSearch
from user import User


def add_user():
    while True:
        name = input("What is your first name?: ").title()
        surname = input("What is your last name?: ").title()
        email = input("What is your email?: ").strip()
        confirm = input("Confirm your email: ").strip()
        if email == confirm:
            proceed = input(f"\nFirst name: {name}\n"
                            f"Last name: {surname}\n"
                            f"Email: {email}\n"
                            f"Do you want to confirm your data? (yes/no/exit): ").lower()
            if proceed == "yes":
                user = User(name=name, surname=surname, email=email)
                user.add_to_sheet()
                break
            elif proceed == "no":
                continue
            else:
                break
        else:
            print("The email you inserted not equal to the confirmation email.\nTry again.")



def add_destination():
    while True:
        add = input("Do you want to add another destination? (yes/no): ")
        if add == "yes":
            destination = input("Destination: ")
            price = int(input("Price: "))
            manager.add_destination(destination=destination, price=price)
        else:
            break


if __name__ == "__main__":
    print("\nWelcome to the Sarritz Flight Club.\nI will find the best flight deals and email them to you.\n")
    while True:
        to_do = input("Type a command:\n(USR): Add user\n(DST): Add destination\n(SRC): Search deals\n(EXT): Exit"
                      "\nCOMMAND: ").upper()
        if to_do == "SRC":
            manager = DataManager()
            notificator = NotificationManager()
            flight_search = FlightSearch(flight_data=manager.get_flight_data(), notificator=notificator)

            print("Starting research..\n")
            flight_search.search()
            for email in manager.get_users_email():
                notificator.send_email(email)
            print("\nDone.")
            break
        elif to_do == "USR":
            add_user()
        elif to_do == "DST":
            add_destination()
        else:
            break
