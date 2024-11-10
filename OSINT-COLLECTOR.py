import requests
import time
import random
import re
import logging
import json
import os
from termcolor import colored

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class APIService:
    def __init__(self, phone_api_key, ip_api_key, timeout=10):
        self.phone_api_key = phone_api_key
        self.ip_api_key = ip_api_key
        self.timeout = timeout

    def validate_key(self):
        test_url = f"http://numverify.com/api/validate?access_key={self.phone_api_key}&number=1234567890"
        try:
            response = requests.get(test_url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("valid", False)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error validating API key: {e}")
            return False

    def phone_info(self, phone_number):
        logging.info(f"Searching for phone number: {phone_number}")
        url = f"http://numverify.com/api/validate?access_key={self.phone_api_key}&number={phone_number}"

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if data.get("valid"):
                self.print_phone_info(data)
            else:
                self.handle_error(data)
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error: {e}")
            print(colored(f"Network error: {e}", "red"))

    def print_phone_info(self, data):
        print(colored(f"\nValid Number: {data.get('number')}", "green"))
        print(f"Location: {data.get('location', 'N/A')}")
        print(f"Carrier: {data.get('carrier', 'N/A')}")
        print(f"Line Type: {data.get('line_type', 'N/A')}\n")

    def handle_error(self, data):
        print(colored("No valid information found for this number.", "red"))
        if data.get("error"):
            print(colored(f"Error: {data['error']['info']}", "red"))

    def ip_info(self, ip_address):
        logging.info(f"Searching for IP: {ip_address}")
        url = f"http://ipapi.co/{ip_address}/json/"

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if 'error' not in data:
                self.print_ip_info(data)
            else:
                print(colored("No valid information found for this IP.", "red"))
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error: {e}")
            print(colored(f"Network error: {e}", "red"))

    def print_ip_info(self, data):
        print(colored(f"\nIP Information for {data.get('ip')}:", "green"))
        print(f"Country: {data.get('country_name', 'N/A')}")
        print(f"Region: {data.get('region', 'N/A')}")
        print(f"City: {data.get('city', 'N/A')}")
        print(f"ISP: {data.get('org', 'N/A')}")
        print(f"Lat/Long: {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}\n")

    def generic_search(self, query):
        logging.info(f"Searching for: {query}")
        url = f"https://api.duckduckgo.com/?q={query}&format=json"

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if 'RelatedTopics' in data and data['RelatedTopics']:
                for topic in data['RelatedTopics']:
                    if 'Text' in topic:
                        print(colored(topic['Text'], "green"))
                        if 'FirstURL' in topic:
                            print(colored(topic['FirstURL'], "blue"))
            else:
                print(colored("No results found.", "red"))
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during search: {e}")
            print(colored(f"Error during search: {e}", "red"))

def is_valid_phone_number(phone_number):
    return re.match(r'^\+\d{1,3}\d{10,}$', phone_number) is not None

def is_valid_ip(ip_address):
    return re.match(r'^(?:\d{1,3}\.){3}\d{1,3}$', ip_address) is not None

def create_api_keys():
    print(colored("To create the JSON configuration file, please provide the following API keys:", "cyan"))
    print("1. Phone API Key: Obtain from https://numverify.com/")
    print("2. IP API Key: Obtain from https://ipapi.co/")

    phone_api_key = input("Enter your Phone API Key: ")
    ip_api_key = input("Enter your IP API Key: ")

    config_data = {
        'phone_api_key': phone_api_key,
        'ip_api_key': ip_api_key,
        'timeout': 10
    }

    with open('config.json', 'w') as f:
        json.dump(config_data, f)
    print(colored("Configuration file 'config.json' created successfully.", "green"))

def load_api_keys():
    config_file = 'config.json'
    if os.path.exists(config_file):
        with open(config_file) as f:
            config = json.load(f)
            return config.get('phone_api_key'), config.get('ip_api_key'), config.get('timeout', 10)
    else:
        print(colored("Configuration file not found. Please create it first.", "red"))
        create_api_keys()
        return load_api_keys()

def load_search_history():
    if os.path.exists('search_history.txt'):
        with open('search_history.txt', 'r') as f:
            return f.readlines()
    return []

def save_search_history(entry):
    with open('search_history.txt', 'a') as f:
        f.write(entry + "\n")

def main():
    print(colored("credit by linux from https://tele.gd/C-WWGKRWAVX", "light_red"))

    phone_api_key, ip_api_key, timeout = load_api_keys()
    if not phone_api_key or not ip_api_key:
        return

    api_service = APIService(phone_api_key, ip_api_key, timeout)

    if not api_service.validate_key():
        print(colored("Invalid Phone API Key. Please check your key and try again.", "red"))
        return

    search_history = load_search_history()

    while True:
        print(colored("[*] ---------------------", "cyan"))
        print(colored("[*] Select the detail to search:", "cyan"))
        print("1. Phone Number (please include country code, e.g., +1234567890)")
        print("2. IP Address (e.g., 192.168.1.1)")
        print("3. Generic Search (e.g., topic or keyword)")
        print("4. View Search History")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == '1':
            phone_number = input("Enter Phone Number: ").strip()
            if is_valid_phone_number(phone_number):
                api_service.phone_info(phone_number)
                save_search_history(f"Phone: {phone_number}")
            else:
                print(colored("Invalid phone number format. Please enter a valid number.", "red"))

        elif choice == '2':
            ip_address = input("Enter IP Address: ").strip()
            if is_valid_ip(ip_address):
                api_service.ip_info(ip_address)
                save_search_history(f"IP: {ip_address}")
            else:
                print(colored("Invalid IP address format. Please enter a valid IP.", "red"))

        elif choice == '3':
            query = input("Enter Generic Search Query: ").strip()
            if query:
                api_service.generic_search(query)
                save_search_history(f"Search: {query}")

        elif choice == '4':
            print(colored("[*] Search History:", "cyan"))
            for entry in load_search_history():
                print(colored(entry.strip(), "yellow"))
        elif choice == '5':
            print(colored("Exiting the program. Goodbye!", "cyan"))
            break
        else:
            print(colored("Invalid choice. Please select a valid option.", "red"))

        wait_time = random.randint(5, 15)
        print(colored(f"[*] Waiting {wait_time} seconds to avoid blocking...", "yellow"))
        time.sleep(wait_time)

if __name__ == "__main__":
    main()
