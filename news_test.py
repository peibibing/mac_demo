# -*- coding: utf-8 -*-
#!/usr/bin/env python
import requests, re, time
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header


def send_mail(path,name):
    sender = '18201251235@163.com'
    # receiver = '2206792067@qq.com'
    receiver = 'huangchao@wordemotion.com'
    subject = '裴必兵'
    smtpserver = 'smtp.163.com'
    username = '18201251235@163.com'
    password = 'myspider1994'
    # part = MIMEApplication(open(path,'rb').read())
    # part.add_header('Content-Disposition', 'attachment', filename=name)

    att2 = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
    att2["Content-Type"] = 'application/octet-stream'
    att2["Content-Disposition"] = 'attachment; filename=%s'%name

    msg = MIMEMultipart()
    msg.attach(att2)
    # msg = MIMEText('dkfvl','plain','utf-8')#中文需参数‘utf-8'，单字节字符不需要
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = 'Novel <18201251235@163.com>'
    msg['To'] = u'超哥 <huangchao@wordemotion.com>'#unicode中文
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    time.sleep(60)#避免大量邮件同时发送造成阻塞

a = requests.get('http://news.sogou.com/news?query=%C5%B7%D6%DE%B1%AD&')
b = a.content.decode('gb18030')
soup = BeautifulSoup(b,"html.parser")
c = soup.div.find_all(class_="vrwrap")#url,title
d = soup.div.find_all(class_="news-from")#source,time
# print(len(d),len(c))
# print(c[2])
work = []

for i in range(10):
    demo = {}
    st = d[i].text
    new_st = re.split(r'\xa0', st)
    demo['source'] = new_st[0]
    demo['time'] = new_st[1]
    demo['title'] = c[i].a.text
    demo['url'] = c[i].a['href']
    print(c[i].a['href'])
    demo['txt'] = c[i].span.text
    work.append(demo)
print(work)
with open('/Users/peibibing/Desktop/test6_18.txt','w') as f:
    f.writelines(repr(work))
# send_mail('/Users/peibibing/Desktop/test6_18.txt','peibibing')

for i in range(len(work)):
    print(work[i]['title'])
# c[0].a['href'] url
# c[0].a.text title
# c[0].span.text  txt
# d[0].text  source,time