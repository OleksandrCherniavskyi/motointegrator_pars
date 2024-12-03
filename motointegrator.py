import requests
from bs4 import BeautifulSoup
import csv


# Function to extract data from each page
def extract_data_from_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all services on the page
        all_services = soup.find_all('div', class_='sc-af971b3c-1 cHwgBe')

        services_data = []
        for service in all_services:
            # Extract the name of the service
            name_tag = service.find('h2', class_='sc-51290aa5-0 hBEGOE sc-2ee0e09c-2 jrlCDw')
            name = name_tag.text.strip() if name_tag else "No Name"

            # Extract the phone number
            phone_tag = service.find('div', class_='sc-eb5621bc-2 bLEcjj')
            phone = phone_tag.text.strip().replace('+48', '').strip() if phone_tag else "No Phone"

            services_data.append([name, phone])

        return services_data
    else:
        print(f"Failed to fetch {url}, status code: {response.status_code}")
        return []


# Function to save the data to a CSV file
def save_to_csv(data, filename='contakt.csv'):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)


# Main loop to iterate over pages and extract data
def scrape_services(start_page=1, end_page=5):
    base_url = 'https://motointegrator.com/pl/pl/warsztaty/katowice?page='

    for page in range(start_page, end_page + 1):
        print(f"Scraping page {page}...")
        url = base_url + str(page)
        services_data = extract_data_from_page(url)

        if services_data:
            save_to_csv(services_data)
        else:
            print(f"No data found on page {page}.")


# Run the scraper for pages 1 to 5 (adjust the range as necessary)
scrape_services(start_page=1, end_page=5)
