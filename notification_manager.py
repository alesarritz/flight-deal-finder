import os
import smtplib

from twilio.rest import Client

account_sid = os.environ["TWILIO_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
email = os.environ["EMAIL"]
password = os.environ["PASSWORD"]


# This class is responsible for sending notifications with the deal flight details.
class NotificationManager:
    def __init__(self):
        self.client = Client(account_sid, auth_token)
        self.message = []

    def send_sms(self):
        self.client.messages.create(body=f"\n{self.message}", from_='+18154568468', to='+393889710599')

    def send_email(self, email_to):
        try:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()  # cript messages
                connection.login(user=email, password=password)
                connection.sendmail(
                    from_addr=email,
                    to_addrs=email_to,
                    msg=f'Subject:Flight Club\n\n{"".join(self.message)}'.encode('utf-8') if self.message != []
                        else "Subject:Flight Club\n\nNo flight found, sorry.",

                )
        except smtplib.SMTPException:
            print("SMTP exception.")

    def add_message(self, msg):
        self.message.append(msg+"\n")
