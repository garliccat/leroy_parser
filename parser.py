# parser for leroymerlin.ru

import requests
from bs4 import BeautifulSoup as bs
import string
import datetime
import csv
import random
import time


def get_html(url):
    user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    ]

    try:
        r = requests.get(url, headers={'User-Agent': random.choice(user_agent_list)}, timeout=10)
    except:
        print('unable to reach page')
        return None

    return r.text


def write_csv(data):
    with open('leroy.csv', 'a', newline='', encoding='UTF-8') as f:
        #newline - to avoid blank rows after each record
        #encoding utf-16 - we are in russia, thats all`
        writer = csv.writer(f, delimiter=';')
        writer.writerow(data)


def get_cats(html):
    ''' fetches the list of categories from catalogue page of leroymerlin
    html: mail catalogue page (https://leroymerlin.ru/catalogue/)
    returns: list of categories urls
    '''
    if html == None:
        print('Page: {} access denied'.format(html))
        return None
    soup = bs(html, 'lxml')
    cats_0 = soup.find_all('div', {'class': 'items-border section-card__items'})
    cats = []
    for cat_0 in cats_0:
        cats_1 = cat_0.find_all('a', href=True)
        for i in cats_1:
            cat = i['href']
            cat = ''.join(['https://leroymerlin.ru', cat])
            cats.append(cat)
    return cats


def get_items(url):
    ''' fetch items info from page of category
    url: url of subpage of category
    returns: writes info into csv (printing it in process)
    '''
    soup = bs(get_html(url), 'lxml')
    cards = soup.find('div', {'class': 'products-container'}).find_all('product-card')
    for card in cards:
        try:
            title = card.find('a', {'slot': 'name'}).get_text(strip=True)
        except:
            title = ''
        print('Title: {}'.format(title))

        try:
            price = card.find('uc-plp-item-price')['content']
        except:
            price = ''
        print('Price: {}'.format(price))

        print()


def get_pages(url):
    ''' fetch subpages from category main page
    url: url of category page
    returns: list of urls of subpages of category, if there is only one page - returns url back
    '''
    pages = []
    try:
        soup = bs(get_html(url), 'lxml')
        pages_num = soup.find('uc-pagination', {'slot': 'pagination'})['total']
        for i in range(1, int(pages_num) + 1):
            pages.append(''.join([url, '?page={}'.format(i)]))
        return pages
    except:
        return url


def main():
    url = 'https://leroymerlin.ru/catalogue/'
    cats_list = get_cats(get_html(url))
    # for i in cats_list[0]:
    #     for j in get_pages(i):
    #         get_items(j)
    get_items(random.choice(get_pages(random.choice(cats_list))))


if __name__ == '__main__':
    main()
