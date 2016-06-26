# -*- coding: utf-8 -*-
# !/usr/bin/env python
from selenium import webdriver
import time, re, requests


def message(mea):
    a = {}
    price = re.findall('<i>(\d.*?)<\/i>', mea)[0]#mea为一个商品的信息
    name = re.findall('<em>(.*?)<\/em>', mea)[1]
    comments = re.findall('#comment">(\d.*?)<\/a>', mea)[0]
    skuid = re.findall('data-sku="(\d*?)"', mea)[0]
    href = 'http:'+re.findall('href="(.*?)"', mea)[0]
    img1 = re.findall('(\/\/img.*jpg)', mea)
    # img1 = re.findall('<imgwidth="200"height="200"data-img="1"src="(.*jpg?)', mea)[0]
    img1 = 'http:'+img1[0]
    s = requests.session()
    img = s.get(img1)
    path_img = '/Users/peibibing/Desktop/jd/img/%s.jpg'%skuid
    with open(path_img, 'wb')as f:
        f.write(img.content)
    a['price'] = price
    a['name'] = name
    a['comments'] = comments
    a['skuid'] = skuid
    a['href'] = href
    a['img'] = img1
    print(a)
    with open('/Users/peibibing/Desktop/jd/message.txt', 'a')as f:
        f.write(repr(a)+',')
        # f.writelines(a)
    return 0


def get_message(url):
    driver =webdriver.PhantomJS()
    # webdriver.Firefox()
    driver.get(url)
    time.sleep(10)

    #.text获取元素的文本数据
    # print(driver.find_element_by_id('content').text)
    a = driver.page_source.encode()
    a1 = a.decode()
    a2 = ''.join(a1.split())
    h = re.findall('<liclass="gl-item">.*?<\/li>', a2)
    print(len(h), h)
    print(h[0])
    # map(message, h)
    for i in range(len(h)):
        print(i)
        message(h[i])







    # c = re.findall('<div class="item-sub" id="category-item-1".*', a1)
    # print(len(c))
    # c1 = re.findall('<div class="dd-inner" style=.*', a1)
    #
    # c2 = re.findall('<div class="dd-inner".*', a1)
    # with open('/Users/peibibing/Desktop/jd/test.txt', 'w')as f:
    #     f.writelines(c2)
    # print(len(c2), c2)
    #关闭浏览器
    driver.close()


def trans_to_comma(x):
    t1 = re.sub('\-', ',', x)
    return t1


def get_url(y):
    url = 'http://list.jd.com/list.html?cat='+y
    return url


if __name__ == '__main__':
    # h = requests.get('http://dc.3.cn/category/get?callback=getCategoryCallback')
    # h1 = h.content.decode('gbk')
    # z = re.findall('(\d+\-\d+\-\d+)\|', h1)
    # ans = list(map(trans_to_comma, z))
    # urls = list(map(get_url, ans))#获取第三级目录url

    url = 'http://list.jd.com/list.html?cat=1713,3263,3394'
    print('test')
    get_message(url)

