#!/usr/local/bin/python3

import requests
from bs4 import BeautifulSoup
import random
import logging


headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/63.0.3239.132 Safari/537.36"}

logging.basicConfig(filename="lxf_git.log", format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)

aimdir = 'lxf_git/'


def randomproxy():
    pros = ["27.213.143.94:8118", "58.249.35.42:8118", "121.30.109.112:80", "183.184.113.143:9797",
            "125.88.177.128:3128", "113.92.3.61:9797", "180.155.139.64:35031", "27.225.187.105:8118"
            ]
    pro = random.choice(pros)
    proxy = {"http": pro, "https": pro}
    return proxy


def downfile(url, filename):
    try:
        proxies = randomproxy()
        print(proxies)
        r = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        content = soup.find('', {'class': 'x-wiki-content x-main-content'})
        for img in content.findAll('img'):
            r = requests.get(img['data-src'], headers=headers, proxies=proxies, timeout=10)
            imgname = img['alt']+'.jpg'
            with open(aimdir+'img/'+imgname, 'wb') as file:
                file.write(r.content)
            logging.info(imgname + " download successfully!")
            img['src'] = 'img/' + imgname
        with open(aimdir+filename, 'w') as file:
            file.write("<!DOCTYPE HTML>\n")
            file.write("<HTML>\n")
            file.write("<BODY>\n")
            file.write(content.prettify())
            file.write("</BODY>\n")
            file.write("</HTML>\n")
        logging.info(filename + " parse successfully!")
    except:
        downfile(url, filename)


def writetoc(toc):
    with open(aimdir+"index.html", 'w') as file:
        file.write("<!DOCTYPE HTML>\n")
        file.write("<HTML>\n")
        file.write("<BODY>\n")
        file.write(toc.prettify())
        file.write("</BODY>\n")
        file.write("</HTML>\n")
    logging.info("index.html write successfully!")


def mainspider():
    indexUrl = "https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000"
    r = requests.get(indexUrl, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    toc = soup.find(id="x-wiki-index").div
    for div in toc.findAll('div'):
        div['style'] = "position:relative;margin-left:15px"
    for link in toc.findAll('a'):
        filename = link.get_text()+".html"
        downfile("https://www.liaoxuefeng.com"+link.attrs['href'], filename)
        link.attrs['href'] = filename
    writetoc(toc)


mainspider()
