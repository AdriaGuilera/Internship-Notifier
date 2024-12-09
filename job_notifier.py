import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# Pushover API Configuration
PUSHOVER_USER_KEY = "uqf6qvuwidzjpauuoyauh7vxarj9iq"  # Replace with your Pushover User Key
PUSHOVER_API_TOKEN = "a4c94cnnjzjhtfkn65jumeqsszydcm"

# Absolute path for the offers file
OFFERS_FILE_PATH = 'todayoffers.json'

# Function to Send Pushover Message
def send_pushover_message(message, link):
    url = "https://api.pushover.net:443/1/messages.json"
    data = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message,
        "url": link
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Message sent to Pushover successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

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

                        message = f"New Job Offer!\n{job}\n{location}"

                        send_pushover_message(message, linktxt)

    save_offers(todayoffers)

if __name__ == "__main__":
    check_new_offers()
    if datetime.now().hour > 21:
        save_offers([])
    else:
        check_new_offers()