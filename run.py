import time
import requests
import configparser
from bs4 import BeautifulSoup
from twilio.rest import Client
from datetime import datetime


def read_config():
    # read configuration file
    config_path = "./config.ini"

    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def send_sms(config, message, img_url=None):
    client = Client(config["Twilio"]["account_sid"], config["Twilio"]["auth_token"])
    if img_url:
        message = client.messages.create(
            body=message,
            from_=config["Twilio"]["from_number"],
            to=config["Twilio"]["to_number"],
            media_url=img_url
        )
    else:
        message = client.messages.create(
            body=message,
            from_=config["Twilio"]["from_number"],
            to=config["Twilio"]["to_number"]
        )
    print(f"Sent message: {message.sid}")


# Stub function for Discord notification (to be implemented)
def send_discord_notification(config, message, img_url):
    pass


# Stub function for WhatsApp notification (to be implemented)
def send_whatsapp_notification(config, message, img_url):
    pass


# Function to fetch the current item from BJJHQ
def fetch_deal_info():
    url = 'https://www.bjjhq.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the description
    meta_description = soup.find('meta', {'property': 'og:description'})['content']
    # Extract the image URL
    img_url = soup.find('meta', {'property': 'og:image'})['content']

    return meta_description, img_url


# Main function to monitor changes and send notifications
def monitor_bjjhq(config, interval=5):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Format down to milliseconds
    print(f"Checking site at {current_time}")

    last_description = None

    while True:
        try:
            description, img_url = fetch_deal_info()

            if description != last_description:
                # Notify about the new deal
                message = f"New deal available: {description}"
                print(message)
                
                # Send a Twilio SMS
                send_sms(config, message, img_url)

                # Stub for Discord and WhatsApp
                send_discord_notification(config, message, img_url)
                send_whatsapp_notification(config, message, img_url)

                last_description = description
            else:
                print("No changes detected.")
        except Exception as e:
            print(f"Error: {e}")

        # Wait before checking again (adjust between 1-3 seconds)
        time.sleep(interval)


# Start the monitoring
if __name__ == "__main__":

    config = read_config()

    monitor_bjjhq(config, interval=3)
