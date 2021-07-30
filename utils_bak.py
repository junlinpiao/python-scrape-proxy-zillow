import json
import random
import time

import deathbycaptcha
import requests
from lxml import html
import pickle

proxy_file_name = 'proxy_http_ip.txt'
PROXIES = []
with open(proxy_file_name, 'rb') as text:
    PROXIES =  [ "http://" + x.decode("utf-8").strip() for x in text.readlines()]

pxy = random.choice(PROXIES)

session = requests.Session()

REQUEST_CNT = 0

def request_with_proxy(url, retry_num=5):
    try:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }

        global pxy
        global REQUEST_CNT

        REQUEST_CNT += 1
        if REQUEST_CNT % 10 == 0:
            pxy = random.choice(PROXIES)

        proxyDict = {
            'http': pxy,
            'https': pxy,
            'ftp': pxy,
            'SOCKS4': pxy
        }
        global session
        r = session.get(url, headers=headers, proxies=proxyDict)
        # r = session.get(url, headers=headers)

        if 'captcha' in r.url or r.status_code != 200:
            pxy = random.choice(PROXIES)
            STATUS_2, STATUS_3, Price = request_with_proxy(url, retry_num=retry_num-1)

        else:
            tree = html.fromstring(r.text)

            try:
                raw_STATUS_2 = tree.xpath('//div[@class="estimates"]//div[@class="status"]//text()')
                STATUS_2 = " ".join(raw_STATUS_2).strip()
            except:
                STATUS_2 = ''

            try:
                STATUS_3 = "".join(tree.xpath('(//div[@class="ds-chip-removable-content"])[1]/p/span[1]//text()')).strip()
            except:
                STATUS_3 = ""

            try:
                raw_Price = tree.xpath('//div[@class="estimates"]//div[@class="price"]//text()')
                Price = " ".join(raw_Price).strip()
            except:
                Price = ''

            if ':' in STATUS_2 and Price == '':
                tmp_STATUS_2 = STATUS_2
                STATUS_2 = tmp_STATUS_2.split(':')[0].strip()
                Price = tmp_STATUS_2.split(':')[1].strip()

            if STATUS_2 == "":
                try:
                    raw_STATUS_2 = tree.xpath('//div[@class="estimates"]/div[1]//text()')
                    STATUS_2 = " ".join(raw_STATUS_2).strip()
                except:
                    STATUS_2 = ''

                try:
                    raw_Price = tree.xpath('//div[@class="estimates"]/div[2]//text()')
                    Price = " ".join(raw_Price).strip()
                except:
                    Price = ''
    except:
        if retry_num == 0:
            return ['', '']
        else:
            pxy = random.choice(PROXIES)
            STATUS_2, STATUS_3, Price = request_with_proxy(url, retry_num=retry_num - 1)

    return STATUS_2, STATUS_3, Price

REQUEST_CNT = 0
Captcha_found = 0  # 0: Captcha is not found, 1: Captcha is now solving

session = requests.Session()
def request_with_proxy_captcha_adv(url, proxy_or_captcha):
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        cookie = "; ".join(["{}={}".format(cookie['name'], cookie['value']) for cookie in cookies])
    except:
        cookie = ""
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,ko;q=0.8",
        "cache-control": "max-age=0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
        "cookie": cookie
    }

    global pxy
    global REQUEST_CNT
    global Captcha_found
    global session

    REQUEST_CNT += 1
    if REQUEST_CNT % 10 == 0:
        pxy = random.choice(PROXIES)

    proxyDict = {
        'http': pxy,
        'https': pxy,
        'ftp': pxy,
        'SOCKS4': pxy
    }

    while Captcha_found == 1:
        time.sleep(0.1)

    # url = "https://www.zillow.com/homedetails/2501-Toron-Ct-Alexandria-VA-22306/51960155_zpid/?fullpage=true"
    if proxy_or_captcha == 1:
        r = session.get(url, headers=headers, proxies=proxyDict)
    else:
        r = session.get(url, headers=headers)

    if 'https://www.zillow.com/captchaPerimeterX' in r.url or r.status_code != 200:
        return 'FAIL', '', '', '', url

    else:
        tree = html.fromstring(r.text)

        try:
            STATUS_2 = tree.xpath('//div[@class="estimates"]//div[@class="status"]/text()')[1].strip()
        except:
            STATUS_2 = ''
        try:
            Price = tree.xpath('//div[@class="estimates"]//div[@class="status"]/span/text()')[1].strip()
        except:
            Price = ''
        try:
            _ = [elm.strip() for elm in tree.xpath('//span[contains(@class, "ds-status-details")]//text()')
                 if elm.strip()]

            STATUS_3 = []
            for elm in _:
                if elm not in STATUS_3:
                    STATUS_3.append(elm)
            STATUS_3 = " ".join(STATUS_3).strip()
        except:
            STATUS_3 = ""

        return 'SUCCESS', STATUS_2, STATUS_3, Price, ''