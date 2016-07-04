# -*- coding: utf-8 -*-
# !/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time, re, requests
from multiprocessing.dummy import Pool as ThreadPool

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
    path_img = '/Users/peibibing/Desktop/jd/img1/%s.jpg'%skuid
    with open(path_img, 'wb')as f:
        f.write(img.content)
    a['price'] = price
    a['name'] = name
    a['comments'] = comments
    a['skuid'] = skuid
    a['href'] = href
    a['img'] = img1
    # print(a)
    with open('/Users/peibibing/Desktop/jd/message1.txt', 'a')as f:
        f.write(repr(a)+',')
        # f.writelines(a)
    return 0


def get_message(url):
    # url = url[:-2]
    driver = webdriver.PhantomJS()
    # webdriver.Firefox()
    # driver.set_page_load_timeout()
    city = WebDriverWait(driver, 10)
    driver.set_page_load_timeout(10)  # 设置selenium的页面加载时间
    try:
        driver.implicitly_wait(10)# 设置selenium的页面加载时间
        driver.get(url)

    except TimeoutError:
        print('time out after 30 seconds when loading page')
        # driver.execute_script('window.stop()')
    time.sleep(10)

    #.text获取元素的文本数据
    # print(driver.find_element_by_id('content').text)
    a = driver.page_source.encode()
    a1 = a.decode()
    a2 = ''.join(a1.split())
    h = re.findall('<liclass="gl-item">.*?<\/li>', a2)
    # print(len(h), h)
    # print(h[58])
    # map(message, h)
    for i in range(len(h)):
        # print(i)
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
    # for i in range(len(urls)):
    #     with open('/Users/peibibing/Desktop/jd/urls.txt', 'a')as f:
    #         f.write(urls[i]+'\n')
    with open('/Users/peibibing/Desktop/jd/urls.txt', 'r')as f:
        urls = f.readlines()
    print(len(urls))
    print(urls[0])
    with open('/Users/peibibing/Desktop/jd/config.txt', 'r')as f:
        a = f.readlines()[0]
        a = int(a)+1

    pool = ThreadPool(4)
    results = pool.map(get_message, urls)
    pool.close()
    pool.join()


    #
    # for i in range(a, len(urls)):
    #     try:
    #         print('url:'+str(i))
    #         time_start = time.time()
    #         get_message(urls[i])
    #         with open('/Users/peibibing/Desktop/jd/config.txt', 'w')as f:
    #             f.writelines(str(i))
    #         perid_time = time.time()-time_start
    #         print(perid_time)
    #     except Exception:
    #         print('error happened')
    #         with open('/Users/peibibing/Desktop/jd/error_config.txt', 'a')as f:
    #             f.writelines(str(i))


    # url = 'http://list.jd.com/list.html?cat=1713,3263,3394'
    # print('test')
    # get_message(url)

