#!/usr/local/bin/python3

import requests
from bs4 import BeautifulSoup
import urllib.request

files = []
images = []
toc_url = "http://tldp.org/LDP/abs/html/"
image_url = "http://tldp.org/LDP/abs/images/"
localdir = "TLDP/html/"


def downfile(url, filename):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    for child in soup.body.findAll("div"):
        if child.attrs['class'] in [['NAVHEADER'], ['NAVFOOTER']]:
            child.decompose()
    with open(localdir + filename, 'w') as file:
        file.write(soup.prettify())
    print(filename + " write successful!")

    for child in soup.findAll("img"):
        img = child.attrs['src'].split("/")[-1]
        if img not in images:
            images.append(img)
            urllib.request.urlretrieve(image_url+img, "TLDP/images/"+img)
            print(img + " download successful!")

    if soup.find('div', {'class': 'TOC'}):
        toc = soup.find('div', {'class': 'TOC'})
        scantoc(toc)


def writeindex(name, url):
    with open(localdir+"index.html", 'a') as file:
        file.write("<a href={}> {} </a><br>".format(url, name))
    print(name + " index write successful!")


def scantoc(toc):
    for link in toc.dl.findAll('a'):
        file_url = link.attrs['href']
        if file_url not in files:
            files.append(file_url)
            writeindex(link.get_text(), file_url)
            downfile(toc_url+file_url, file_url)


with open(localdir+"index.html", 'w') as file:
    file.write("<!DOCTYPE HTML>\n")
    file.write("<HTML>\n")
    file.write("<BODY>\n")

html = requests.get(toc_url)
soup = BeautifulSoup(html.text, "html.parser")
toc = soup.find('div', {'class': 'TOC'})
scantoc(toc)

with open(localdir+"index.html", 'a') as file:
    file.write("</HTML>\n")
    file.write("</BODY>\n")
