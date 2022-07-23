import requests
import json
from bs4 import BeautifulSoup

def do_normal_href(start, middle, end):
    list = []
    for href in middle:
        list.append(start + href + end)

    return list

# Сохранение списка
def save_data(list, filename):
    with open(filename + '.json', 'w') as output_file:
        json.dump(list, output_file)

# Достаем имеющиеся коины на первой странице (следующие страницы, думаю не имеет смысла парсить из-за маленькой ликвидности)
def get_href(headers, url):
    all_href_coins = []

    # Доостаем весь html
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, 'lxml')

    # Найдем все теги в таблице
    coins = soup.find('tbody')

    # Найдем ссылки на все монеты
    for link in coins.find_all('a', class_ = 'cmc-link'):
        if not('markets' in link.get('href') or '?period=7d' in link.get('href')):
            all_href_coins.append(link.get('href'))

    return all_href_coins

def get_market():
    headers = {
        'authority': 'api.coinmarketcap.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9',
        'if-modified-since': 'Sun, 03 Jul 2022 21:36:23 GMT',
        'origin': 'https://coinmarketcap.com',
        'platform': 'web',
        'referer': 'https://coinmarketcap.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Yandex";v="22"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.4.904 Yowser/2.5 Safari/537.36',
        'x-request-id': '2927b3e760a9470c9d388f803c0c8a90',
    }

    params = {
        'slug': 'bitcoin',
        'start': '1',
        'limit': '100',
        'category': 'spot',
        'sort': 'cmc_rank_advanced',
    }
    all_markets = []

    # Получаем весь html страницы
    request = requests.get('https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest', headers = headers, params = params)
    soup = BeautifulSoup(request.text, 'lxml')
    print(request.status_code)

    # Найдем все коины в таблице
    for market in soup.find_all('p', class_ = 'sc-1eb5slv-0 iworPT'):
        all_markets.append(market.text)
    print(all_markets)

    return all_markets

def get_pairs(headers, url):
    pass

def get_price(headers, url):
    pass

def main():
    url = 'https://coinmarketcap.com'
    headers = {
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) Chrome/100.0.4896.160 YaBrowser/22.5.4.904 Yowser/2.5'
    }
    trading_pairs = {}

    href = get_href(headers, url)

    # Сделаем правильные ссылки
    for i in range(len(href)):
        href[i] = url + href[i] + 'markets/'
    # print(href)

    # Сохраним эти ссылки в json
    save_data(href, 'coins')

    # Будем передавать в функцию ссылку на маркет и получать список: Площадка, Пара, Цена
    # for link in href:
        # trading_pairs['market'] = get_market(headers, link)
        # trading_pairs['pairs'] = get_pairs(headers, link)
        # trading_pairs['price'] = get_price(headers, link)

    print(href[0])
    print(get_market())
if __name__ == '__main__':
    main()
