from twilio.rest import Client
import smtplib
import os


class NotificationManager:
    ACCOUNT_SID = os.getenv("ACCOUNT_SID")
    SMS_AUTH_TOKEN = os.getenv("SMS_AUTH_TOKEN")
    MY_PHONE_NUMBER = "+421949737448"
    MY_EMAIL = "viktor.milosavljevic2@gmail.com"
    MY_EMAIL_PASSWORD = os.getenv("MY_EMAIL_PASSWORD")
    client = Client(ACCOUNT_SID, SMS_AUTH_TOKEN)

    def send_message(self, flight_data):
        self.client.messages.create(
            to=self.MY_PHONE_NUMBER,
            from_="+19122083725",
            body=f"Found a cheap flight from {flight_data['from']} to {flight_data['to']} on {flight_data['departure_date']} returning on {flight_data['return_date']} for {flight_data['price']} EUR!",
        )

    def send_email(self, flight_data, email):
        flight_google_link = f"https://www.google.sk/flights?hl=sk#flt={flight_data['from_airport']}.{flight_data['to_airport']}.{flight_data['departure_date']}*{flight_data['to_airport']}.{flight_data['from_airport']}.{flight_data['return_date']}"

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.MY_EMAIL, password=self.MY_EMAIL_PASSWORD)
            connection.sendmail(
                from_addr=self.MY_EMAIL,
                to_addrs=email,
                msg=f"Subject:Cheap Flight Found!\n\nFound a cheap flight from {flight_data['from']} ({flight_data['from_airport']}) to {flight_data['to']} ({flight_data['to_airport']})!\n\n{flight_data['nights_in_destination']} nights from {flight_data['departure_date']} to {flight_data['return_date']} for {flight_data['price']} EUR!\n\nGoogle link: {flight_google_link}",
            )

