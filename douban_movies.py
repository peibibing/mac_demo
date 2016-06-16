# -*- coding: utf-8 -*-
#!/usr/bin/env python
import requests, re, urllib, time
from threading import Lock, Thread
from queue import Queue


class Fetcher:
    def __init__(self,threads):
        self.opener = urllib.request.build_opener(urllib.request.HTTPHandler)
        self.lock = Lock()
        self.q_req = Queue()
        self.q_ans = Queue()
        self.threads = threads
        for i in range(threads):
            t = Thread(target=self.threadget)
            t.setDaemon(True)
            t.start()
        self.running = 0


    def __del__(self):
        time.sleep(0.5)
        self.q_req.join()
        self.q_ans.join()

    def taskleft(self):
        return self.q_req.qsize()+self.q_ans.qsize()+self.running

    def push(self,req):
        self.q_req.put(req)


    def pop(self,ans):
        return self.q_ans.get()

    def threadget(self):
        while True:
            req = self.q_req.get()
            with self.lock:  #保证操作的原子性
                self.running += 1
            try:
                ans = self.opener.open(req).read()
            except Exception:
                ans = 'error'
                print(ans)
            self.q_ans.put((req,ans))
            with self.lock:
                self.running -= 1
            self.q_req.task_done()
            time.sleep(0.1)


def download_imag(subject):
    global count
    s = requests.session()
    imag = s.get(subject['cover'])
    name = subject['title']
    path = '/users/peibibing/PycharmProjects/douban/douban_movie/%s.jpg'%name
    with open(path,'wb') as f:
        f.write(imag.content)
    count += 1
    print(count)
    return 'ok'


def get_subject(url):
    header={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Host':'movie.douban.com',
        'Connection':'keep-alive'
    }
    a = requests.get(url=url)
    b = a.json()['subjects']
    # print(len(b),b[0]['cover'],b[0]['title'])
    return b

count = 0
if __name__ == "__main__":
    
    num = 20
    url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=6000&page_start=0'
    subjects = get_subject(url)
    # print(subjects[0])
    end = list(map(download_imag,subjects))
    # print(len(end))
    # f = Fetcher(threads=10)
    # map(f.push(),)
