#! /usr/local/bin/python3

import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
import sys

headers = {
    "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 "
        "Safari/537.36 "
}


def login():
    postdata = {
        "name": "guhangsong@163.com",
        "password": "guhangsong1117",
    }

    login_url = 'https://accounts.douban.com/j/mobile/login/basic'

    session = requests.session()
    r = session.get(login_url, headers=headers)
    soap = BeautifulSoup(r.text, "html.parser")
    if soap.find(id='captcha_image'):
        captcha_url = soap.find(id='captcha_image')['src']
        captcha_id = soap.find('', {'name': 'captcha-id'})['value']
        urllib.request.urlretrieve(captcha_url, "captcha.jpg")
        postdata["captcha-solution"] = input("Read the picture number: ")
        postdata["captcha-id"] = captcha_id

    r = session.post(login_url, data=postdata, headers=headers)
    soap = BeautifulSoup(r.text, "html.parser")
    if r.status_code == 200 and r.cookies:
#    if r.status_code == 200:
        print("login success")
    else:
        print(r.status_code)
        print(r.raw)
        for i, v in r.cookies.items():
            print(i, v)
        sys.exit("login fail, check your network, email or password")

    r = session.get("https://www.douban.com/people/1000001/", headers=headers)
    soap = BeautifulSoup(r.text, "html.parser")
    print(soap.find(id='common').h2.get_text())

    return session


login()


def common_spider():
    file = "douban_common1.csv"
    with open(file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for id in range(1001105, 172605625):
            #            session = requests.session()
            #            if id % 500 == 0:

            soap = BeautifulSoup(r.text, "html.parser")

            # s = soap.find(id='common').h2.get_text()
            # common = int(s[s.find("(")+1:s.find(")")])
            # line = [id, common]
            # writer.writerow(line)
            #            with open('soap', 'w') as f:
            #                f.write(soap.string)
            #            print(soap.find(id='common').h2.get_text())
            try:
                s = soap.find(id='common').h2.get_text()
                common = int(s[s.find("(") + 1:s.find(")")])
                line = [id, common]
                writer.writerow(line)
                print(str(id) + ":已写入文件")
            except:
                if soap.find("title").get_text() == "页面不存在":
                    print(str(id) + ":页面不存在")
                    continue
                else:
                    print(str(id) + ":无共同爱好")
                    continue

#    print(soap.find(id='common').h2.get_text())

# common_spider()
