import requests
from bs4 import BeautifulSoup
import csv
import time
from random import randint

with open('gaming_mice.csv', 'w', encoding='utf-8', newline='') as file:
    write_obj = csv.writer(file)
    write_obj.writerow(['Brand', 'Model', 'Price', 'Link'])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for page_num in range(1, 6):
        url = f'https://mouse.ge/catalog/gamingmouse/page-{page_num}'
        response = requests.get(url, headers=headers)
        print(f'Fetching page {page_num}: {response.status_code}')

        if response.status_code != 200:
            print(f'Failed to fetch page {page_num}')
            continue

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        products = soup.find_all('div', class_='product-layout')

        if not products:
            print(f'No products found on page {page_num}')
            continue

        for product in products:
            try:
                brand = product.find('div', class_='manufacturer').text.strip()
                model = product.find('h4', class_='product-title').text.strip()
                price = product.find('span', class_='price').text.strip()
                link = product.find('h4', class_='product-title').a['href']

                write_obj.writerow([brand, model, price, link])
                print(f'Scraped: {brand} {model} - {price}')
            except Exception as e:
                print(f'Error scraping product: {e}')

        print(f'Completed page {page_num}: {url}')

        time.sleep(randint(15, 20))

print('Scraping complete!')
