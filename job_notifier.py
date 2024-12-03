from twilio.rest import Client
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# Twilio API Configuration
TWILIO_ACCOUNT_SID = "AC9ab6fd78eec22b87541d798d38471ba2"
TWILIO_AUTH_TOKEN = "00c490583148ff3d6baa534032df7fa1"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"
MY_WHATSAPP_NUMBER = "whatsapp:+34685172041"

# Absolute path for the offers file
OFFERS_FILE_PATH = '/home/your_username/job_notifier/todayoffers.json'

# Function to Send WhatsApp Message
def send_whatsapp_message(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=MY_WHATSAPP_NUMBER
    )
    print(f"Message sent: {message.sid}")

# Function to load offers from a JSON file
def load_offers():
    try:
        with open(OFFERS_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save offers to a JSON file
def save_offers(offers):
    with open(OFFERS_FILE_PATH, 'w') as file:
        json.dump(offers, file)

def clean_offers():
    try:
        with open(OFFERS_FILE_PATH, 'w') as file:
            json.dump([], file)
    except FileNotFoundError:
        return []

# Function to Check New Job Offers
def check_new_offers():
    todayoffers = load_offers()

    for i in range(0, 3):
        URL = "https://borsapractiques.fib.upc.edu/ca/ofertes_ltd?page=" + str(i)
        response = requests.get(URL)
        if response.status_code != 200:
            print(f"Error accessing the website: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, 'lxml')
        for offer in soup.select('.vip-'):
            date_element = offer.select_one('.datetime')
            job_element = offer.select_one('.use-ajax')
            location_element = offer.select_one('.views-field.views-field-address__administrative-area')

            if date_element and job_element and location_element:
                if date_element.text == datetime.now().strftime('%d/%m/%Y'):
                    job = job_element.text.strip()
                    link = job_element['href']
                    location = location_element.text.strip()
                    if job not in todayoffers:
                        todayoffers.append(job)
                        linktxt = f"https://borsapractiques.fib.upc.edu/ca/ofertes/oferta/{link[-4:]}"

                        print(job)
                        print(location)
                        print(linktxt)

                        message = f"*New Job Offer!*\n{job}\n{location}\n{linktxt}"
                        send_whatsapp_message(message)

    save_offers(todayoffers)

if __name__ == "__main__":
    check_new_offers()
    if datetime.now().hour > 20:
        save_offers([])