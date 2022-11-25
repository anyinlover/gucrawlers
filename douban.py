from selenium import webdriver
import pandas as pd
import re

def restart():
    global driver
    driver.close()
 #   driver = webdriver.Chrome(chrome_options=option)
    driver = webdriver.Chrome()
    driver.get("https://book.douban.com/")
    print("restart browser")

def getdouban(row):
    if int(row['index']) % 50 == 0:
        restart()

    isbn = row["isbn"]
    if (len(isbn) > 13) & ("978" in isbn):
        i = isbn.find("978")
        isbn = isbn[i:i+13]
    if (len(isbn) == 13) & (isbn.startswith("978")):
        sbox = driver.find_element_by_xpath("//input[@id='inp-query']")
        sbox.clear()
        sbox.send_keys(isbn)
        sbox.submit()
        people = driver.find_element_by_xpath("//span[@class='pl']").text
        if people == "(评价人数不足)" or "(目前无人评价)":
            star = "0"
            ps = "0"
        else:
            ps = re.sub("\D", "", people)
            star = driver.find_element_by_xpath("//span[@class='rating_nums']").text
        row["douban"] = star
        row["people"] = ps
        print("{}: {} {} done!".format(row["index"], isbn, star)）
    return row

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome()
# driver = webdriver.Chrome(options=option)
driver.get("https://book.douban.com/")

df = pd.read_csv("my_books6.csv", dtype=str, keep_default_na=False)
df["people"] = ""
df1 = df.loc[:1]
try:
    for index, row in df1.iterrows():
        df1.loc[index] = getdouban(row)
finally:
    df.to_csv("my_books70.csv", index=False)
#    driver.close()