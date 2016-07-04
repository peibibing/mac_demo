# -*- coding: utf-8 -*-
# !/usr/bin/env python
import requests, re, random
from bs4 import BeautifulSoup


def proxies_pool(url):
    ips = []
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}
    a = requests.get(url, headers=headers)
    b = a.content.decode()
    soup = BeautifulSoup(b, "html.parser")
    c = soup.table.find_all(class_="odd")

    # print(len(d), type(d), d[0][], d)
    for i in range(len(c)):
        proxies = {}
        d = c[i].find_all('td')
        ip = repr(d[1])
        port = repr(d[2])
        ip = re.findall('>(.*)<', ip)[0]
        port = re.findall('>(.*)<', port)[0]

        pro = 'http://'+ip+':'+port
        proxies['http'] = pro
        ips.append(proxies)
    return ips


def get_proxies_ip(url):
    ips = proxies_pool(url=url)
    # print(len(ips))
    ip = random.choice(ips)
    return ip


if __name__ == '__main__':
    url1 = 'http://www.xicidaili.com/'
    proxies = get_proxies_ip(url1)
    print(proxies)





