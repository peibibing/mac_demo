# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/date/
# import urllib3
import urllib
from threading import Thread,Lock
from multiprocessing import Pool
import requests
from queue import Queue
import time
import re


class Fetcher:
    def __init__(self,threads):

        self.opener = urllib.request.build_opener(urllib.request.HTTPHandler)
        self.lock = Lock() #线程锁
        self.q_req = Queue() #任务队列
        self.q_ans = Queue() #完成队列
        self.threads = threads
        for i in range(threads):
            t = Thread(target=self.threadget)
            t.setDaemon(True)
            t.start()
        self.running = 0

    def __del__(self): #解构时需等待两个队列完成
        time.sleep(0.5)
        self.q_req.join()
        self.q_ans.join()

    def taskleft(self):
        return self.q_req.qsize()+self.q_ans.qsize()+self.running

    def push(self,req):
        self.q_req.put(req)

    def pop(self):
        return self.q_ans.get()

    def threadget(self):
        while True:
            req = self.q_req.get()
            with self.lock: #要保证该操作的原子性，进入critical area
                self.running += 1
            try:
                ans = self.opener.open(req).read()
            except Exception:
                ans = ''
                print (ans)
            self.q_ans.put((req,ans))
            with self.lock:
                self.running -= 1
            self.q_req.task_done()
            time.sleep(0.1) # don't spam

if __name__ == "__main__":

    # print links[0:10]
    f = Fetcher(threads=100)


    num_count = 0
    h=open('/home/peibibing/data/bibing_test.txt','r').readlines()

    # h = h[1937573:]

    h = h[1937430:]

    # f=open('/home/peibibing/test1.txt','r')
    # print h[1]
    s=open('/home/peibibing/thread_result1.txt','w')
    #
    # num_count=0
    # for x in h:
    #     num_count += 1
    #     # print num_count
    #     # print x
    #     x=int(x)

    links = [ 'http://club.jd.com/clubservice.aspx?method=GetCommentsCount&referenceIds=%d&callback=jQuery6374420&_=1462441504406'%int(i) for i in h]
    # print links[0:10]
    f = Fetcher(threads=100)
    for url in links:
        f.push(url)
    while f.taskleft():
        num_count += 1
        print (num_count)
        url,content = f.pop()
        # test1 = content.read()
        # print test1
        # print content
        frist_result=re.search('referenceIds=\d+',url)
        jd_id=re.search('\d+',frist_result.group())
        try:
            TextSplit=re.split(',',content)[8]
            a=re.split(':',TextSplit)[1]
        except Exception:
            # TextSplit=re.split(',',content)[8]
            # if not TextSplit:
            #     continue
            # a=re.split(':',TextSplit)[1]
            # c=re.search('CommentCount',a)
            # if not c.group():
            #     continue
            continue
            # TextSplit=re.split(',',content)[8]
            # a=re.split(':',TextSplit)[1]


        # TextSplit=re.split(',',content)[8]

        # print TextSplit
        # print TextSplit
        # print len(TextSplit)
        # a=re.split(':',TextSplit)[1]
        # print url,len(content)
        # s.writelines(a)

        s.writelines(str(jd_id.group()))
        s.writelines(',')
        s.writelines(str(a))
        s.writelines('\n')
    # h.close()
        s.close()

