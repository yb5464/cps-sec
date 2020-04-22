from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time

path = os.getcwd() + "\\6th\chromedriver.exe"
driver = webdriver.Chrome(path)

try:
    driver.get("http://www.kyobobook.co.kr/index.laf?OV_REFFER=https://www.google.com/")
    time.sleep(1)

    #searchIndex에 검색할 책의 키워드를 넣는다.
    searchIndex = "축구"
    element = driver.find_element_by_class_name("main_input")
    element.send_keys(searchIndex)
    #검색 버튼을 클릭한다.
    driver.find_element_by_class_name("btn_search").click()

    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")

    title = list()
    for i in range(3):
        time.sleep(1)

        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")     

        conts = bs.find("div", class_ = "list_search_result").find_all("td", class_ = "detail")

        title.append("page " + str(i + 1))
        for c in conts:
            title.append(c.find("div", class_ = "title").find("strong").text)

        driver.find_element_by_xpath('//*[@id="contents_section"]/div[9]/div[1]/a[3]/img').click()



finally:
    for j in title:
        if j.find("page ") != -1:
            print()
        print(j)

    time.sleep(3)
    driver.quit()
