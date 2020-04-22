from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time

path = os.getcwd() + "\\6th\chromedriver.exe"

driver = webdriver.Chrome(path)

#try 밑에있는 어떤 코드가 실행이 되고 실행이 다 됐다면 finally에 있는 코드가 실행
try:
    driver.get("https://www.cau.ac.kr/cms/FR_CON/index.do?MENU_ID=2130#page1")
    #driver.get이라는 함수를 통해서 url에 접근하게 될 때 페이지 로딩 시간이 필요함. 시간 조절이 필요함
    time.sleep(1)       #driver.implicitly_wait(10) 으로 대체할 수 있음. 로딩이 끝날 때 까지 기다려줌

    #requests.get().text와 같은 기능
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")

    #find_all은 return type이 list이다.
    #find_all("a")[-1]["href"]는 a태그를 모두 찾아 리스트로 리턴 받고
    #그 리턴 값 중 맨 마지막 중 href라는 클래스의 내용만 찾겠다. 이다.
    pages = bs.find("div", class_ = "pagination").find_all("a")[-1]["href"].split("page")[1]
    pages = int(pages)
    
    title = list()
    for i in range(2):
        driver.get("https://www.cau.ac.kr/cms/FR_CON/index.do?MENU_ID=2130#page" + str(i + 1))
        time.sleep(3)

        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")

        conts = bs.find_all("div", class_ = "txtL")
        title.append("page" + str(i + 1))

        for c in conts:
            title.append(c.find("a").text.strip())

finally:
    time.sleep(2)
    for j in title:
        if j.find("page") != -1:
            print("\n")
        print(j)

    driver.quit()
