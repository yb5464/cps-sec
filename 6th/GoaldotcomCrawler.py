from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time
import csv

def writeCSV(newsTitle, pages):
    file = open('GoaldotcomCrawler.csv','a', newline='')
    line = csv.writer(file)

    for i in range(len(newsTitle)):
        line.writerow([str(i + 1), newsTitle[i]])
    
    file.close()

path = os.getcwd() + "\\6th\chromedriver.exe"
driver = webdriver.Chrome(path)

file = open('GoaldotcomCrawler.csv','w', newline='')
line = csv.writer(file)
line.writerow(["No", "Title"])
file.close()

#try 밑에있는 어떤 코드가 실행이 되고 실행이 다 됐다면 finally에 있는 코드가 실행
try:
    driver.get("https://www.goal.com/kr/%EC%9D%B4%EC%A0%81-%EB%89%B4%EC%8A%A4")
    #driver.get이라는 함수를 통해서 url에 접근하게 될 때 페이지 로딩 시간이 필요함. 시간 조절이 필요함
    driver.implicitly_wait(10)

    #requests.get().text와 같은 기능c
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")


    #제가 크롤링 한 goal.com은 과거의 이적 루머를 지우는 것이 아니라 남겨두기 때문에 page number으로 접근한다면
    #너무 많은 정보들이 생성됩니다. 따라서 사용자에게 몇 페이지까지 얻을 것인지 입력값을 받습니다.
    pages = int(input("몇 페이지까지 찾을까요? (1페이지에는 총 30개의 이적루머가 있습니다.): "))
    title = list()


    for i in range(pages):
        driver.get("https://www.goal.com/kr/%EC%9D%B4%EC%A0%81-%EB%89%B4%EC%8A%A4/" + str(i + 1))
        driver.implicitly_wait(10)

        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")

        cont = bs.find_all("div", class_ = "title")

        
        for c in cont:
            title.append(c.find("h3").text)



finally:
    time.sleep(2)
    writeCSV(title, pages)
    driver.quit()
