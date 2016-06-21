# -*- coding: utf-8 -*-
#!/usr/bin/env python
from selenium import webdriver
import time, re, requests


def get_message(url):
    driver =webdriver.PhantomJS()
    webdriver.Firefox()
    driver.get(url)
    time.sleep(10)

    #.text获取元素的文本数据
    # print(driver.find_element_by_id('content').text)
    a = driver.page_source.encode('gbk')
    a1 = repr(a)

    c = re.findall('<div class="item-sub" id="category-item-1".*', a1)
    print(len(c))
    c1 = re.findall('<div class="dd-inner" style=.*', a1)

    c2 = re.findall('<div class="dd-inner".*', a1)
    with open('/Users/peibibing/Desktop/jd/test.txt', 'w')as f:
        f.writelines(c2)
    print(len(c2), c2)
    #关闭浏览器
    driver.close()


def trans_to_comma(x):
    t1 = re.sub('\-', ',', x)
    return t1


def get_url(y):
    url = 'http://list.jd.com/list.html?cat='+y
    return url

def main():
    return 0


if __name__ == '__main__':
    h = requests.get('http://dc.3.cn/category/get?callback=getCategoryCallback')
    h1 = h.content.decode('gbk')
    z = re.findall('(\d+\-\d+\-\d+)\|', h1)
    ans = list(map(trans_to_comma, z))
    urls = list(map(get_url, ans))

 a2 = ''.join(a1.split())
 re.findall('<liclass="gl-item">.*?<\/li>',a2)[0]


