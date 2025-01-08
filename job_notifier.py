import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os

# Pushover API Configuration
PUSHOVER_USER_KEY = os.getenv('PUSH_USER_KEY')
PUSHOVER_API_TOKEN = os.getenv('PUSH_API_KEY')

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

# Function to Check New Job Offers
def check_new_offers():
    for i in range(0, 2):
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
                date = datetime.fromisoformat(date_element['datetime'])
                if date.strftime('%d/%m/%Y') == datetime.now(date.tzinfo).strftime('%d/%m/%Y'):
                    if date > datetime.now(date.tzinfo) - timedelta(minutes=30):
                        job = job_element.text.strip()
                        link = "https://borsapractiques.fib.upc.edu/ca/ofertes/oferta/" + job_element['href'][-4:]
                        location = location_element.text.strip()
                        print(job)
                        print(location)
                        print(link)
                        message = f"New Job Offer!\n{job}\n{location}"
                        send_pushover_message(message, link)

if __name__ == "__main__":
    check_new_offers()