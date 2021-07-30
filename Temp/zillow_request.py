import requests
from lxml import html
import re
import random

sess = requests.Session()
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
}

urls = [
    "https://www.zillow.com/homedetails/5931-Peverill-Dr-Alexandria-VA-22310/51922494_zpid/",
    "https://www.zillow.com/homedetails/3208-Spring-Dr-Alexandria-VA-22306/51954225_zpid/",
    "https://www.zillow.com/homedetails/1-Ocean-Dr-E10A-Brooklyn-NY-11224/2080353059_zpid/",
    "https://www.zillow.com/homedetails/385-Graham-Ave-APT-4R-Brooklyn-NY-11211/2099162718_zpid/",
    "https://www.zillow.com/homedetails/199-Bay-Ter-Staten-Island-NY-10306/32345094_zpid/",
    "https://www.zillow.com/homedetails/7413-Duddington-Dr-Alexandria-VA-22315/51951825_zpid/"
]

PROXY_GATEWAY_POOL = [
    "45.149.145.82:8000:4apYHC:dD32xW", "45.149.144.240:8000:4apYHC:dD32xW",
    "45.149.146.66:8000:4apYHC:dD32xW", "45.149.145.77:8000:4apYHC:dD32xW",
    "45.149.145.187:8000:4apYHC:dD32xW", "45.149.146.65:8000:4apYHC:dD32xW",
    "45.149.147.129:8000:4apYHC:dD32xW", "45.149.147.16:8000:4apYHC:dD32xW",
    "45.149.145.211:8000:4apYHC:dD32xW", "45.149.147.202:8000:4apYHC:dD32xW",
    "45.149.145.247:8000:4apYHC:dD32xW", "45.149.146.9:8000:4apYHC:dD32xW",
    "45.149.144.94:8000:TtnqZk:oeLsgH"
]  # ,


for url in urls:
    proxy = random.choice(PROXY_GATEWAY_POOL)
    pxy = 'http://{2}:{3}@{0}:{1}'.format(*proxy.split(':'))
    proxyDict = {
        'http': pxy,
        'https': pxy,
        'ftp': pxy,
        'SOCKS4': pxy
    }
    sess.proxies = proxyDict

    r = sess.get(url=url, headers=headers)
    print(r.url)
    tree = html.fromstring(r.text)

    try:
        status = [elm.strip() for elm in tree.xpath('(//span[contains(@class, "ds-status-details")])[1]//text()') if
                  elm.strip()][0].strip()
    except:
        status = ""

    if status == "Sold":
        try:
            description = tree.xpath('//meta[@property="zillow_fb:description"]/@content')[0].strip()
        except:
            description = ""
        try:
            price = re.findall(r'(\$[0-9\,]+)', description)[0]
        except:
            price = ""

        STATUS_2 = status
        STATUS_3 = ""
        Price = price
    else:
        STATUS_2 = ""
        STATUS_3 = status
        Price = ""

    print([STATUS_2, STATUS_3, Price])
