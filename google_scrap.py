import json
from selenium import webdriver

def google_scrap(queries, dir):
    with webdriver.Chrome() as driver:
        parse_data = []
        for query in queries:
            new_query = query.replace(" ", "+")
            search_url = f"https://www.google.com/search?hl=en&q={new_query}&cr=countryUS"
            driver.get(search_url)

            page_parser(driver, parse_data)
            next_page = driver.find_element_by_xpath("//a[@id='pnnext")
            next_page.click()
    
    result_df = pd.DataFrame(parse_data)
    result_df.to_excel("all.xlsx", index=False)


def page_parser(driver, parse_data):
    tree = driver.find_element_by_xpath("//div[@id='rso']/div[@class='g']")
    for node in tree:
        url = node.find_element_by_xpath(".//a").get_attribute("href")
        title = node.find_element_by_xpath(".//h3").text
        desc = node.find_element_by_xpath(".//div[@class='IsZvec']").text

        parse_data.append()