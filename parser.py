import csv

import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import time

ua = UserAgent()
HEADERS = {'User-Agent': ua.random}

# search_collection = bot.active_collection

print('Example https://www.work.ua/ru/jobs-kyiv/')
CITY = input('To parse kyiv write "-", to parse another city send link: ')
if CITY != '-':
    URL = CITY
else:
    URL = f'https://www.work.ua/ru/jobs-kyiv/'

# COUNT_OF_PAGE = int(input('Write count of page or all: '))

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages(html):
    soup = bs(html.text, 'html.parser')
    full = soup.find('div', id='pjax-job-list')
    max_page = full.find('ul', class_='pagination').text.split()[-2]
    return max_page


def get_content(html):
    soup = bs(html.text, 'html.parser')
    full = soup.find('div', id='pjax-job-list')
    work_card = full.findAll('div', class_='card-hover')
    work_cards = []
    for item in work_card:

        title = item.find('h2').get_text(strip=True)

        url = 'https://www.work.ua' + item.find('a').get('href').strip()

        if item.find('b').get_text(strip=True).split()[-1] == 'грн':
            price = item.find('b').get_text(strip=True)
        else:
            price = '-'

        overview = item.find('p', class_='overflow').get_text(strip=True)
        work_cards.append({
            'title': title,
            'url': url,
            'price': price,
            'overview': overview
        })
    return work_cards


def save_csv(items):
    with open('work.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Url', 'Price', 'Overview'])
        for item in items:
            writer.writerow([item['title'], item['url'], item['price'], item['overview']])


def parsing():
    html_get = get_html(URL)
    if html_get.status_code == 200:
        work_content = []
        page_count = get_pages(html_get)

        number_of_page = int(page_count)
        print(f'Total pages - {number_of_page}')
        count_of_page = input('Write count of page or all: ')
        if count_of_page == 'all':
            count = int(page_count)
        else:
            count = int(count_of_page)+1
        for page in range(1, count):
            count -= 1
            html = get_html(URL, params={'page': page})
            work_content.extend(get_content(html))
            print(f'Left {int(count - 1)} pages | Vacancies were parsed {len(work_content)}')

        save_csv(work_content)

    else:
        print('Something went wrong :(')


if __name__ == '__main__':
    parsing()

