'''
1. 웹사이트 접속
2. 웹사이트 html로 받아오기
3. html에서 원하는 정보 찾기
4. 수집

제가 만든 파일은 실행과 동시에 검색어와 출력 페이지 개수를 받아서
입력된 출력 페이지 만큼 네이버 뉴스를 불러온 뒤, 뉴스 제목, 링크, 출처를 출력합니다.
'''
from bs4 import BeautifulSoup
import requests
import csv

class Scraper :
    def __init__(self, word, cnt):
        url_left = "https://search.naver.com/search.naver?&where=news&query="
        url_right = "&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=26&start="
        self.url = url_left + str(word) + url_right
        self.cnt = cnt
        self.tried = 0
        #사용자에게 입력받은 검색어를 URL중간에 삽입하여 검색어에 맞는 뉴스가 검색되게 만듬
        #cnt는 페이지의 개수를 담아둘 변수로 tried를 1개씩 늘리면서 cnt와 같아질 때 까지 페이지를 출력할 계획

    def getHTML(self, cnt):
        res = requests.get(self.url + str(cnt * 10 + 1))

        if res.status_code != 200:
            print("잘못된 접근입니다.", res.status_code)

        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        return soup
        
    def getNews(self, soup):
        contents = soup.find_all(class_ = "_sp_each_title")
        source = soup.find_all(class_ = "_sp_each_source")

        newsTitle = list()
        newsLink = list()
        newsSource = list()

        for i in range(len(contents)):
            newsTitle.append(contents[i].attrs["title"].strip())
            newsLink.append(contents[i].attrs["href"].strip())
            newsSource.append(source[i].text.strip())
        #링크와 타이틀은 _sp_each_title에서, 출처는 _sp_each_source에서 각각 얻어야 했기 때문에 soup을 두번 사용함
        #리스트 메소드 strip을 이용해서 문자열 좌우를 깔끔하게 다듬고 append 함

        self.writeCSV(newsTitle, newsLink, newsSource)
        
    def writeCSV(self, newsTitle, newsLink, newsSource):
        file = open('4th_practice_news.csv','a', newline='')
        line = csv.writer(file)

        for i in range(len(newsTitle)):
            line.writerow([str(i + 1 + self.tried * 10), newsTitle[i], newsSource[i], newsLink[i]])
        
        file.close()

    def scrap(self):

        file = open('4th_practice_news.csv','w', newline='')
        line = csv.writer(file)
        line.writerow(["No", "Title","Source", "Link"])
        file.close()

        while self.tried < self.cnt:
            soup = self.getHTML(self.tried)
            self.getNews(soup)
            self.tried += 1
        #실습예시와 다른 방법으로 페이지를 출력하기 위해 고안해낸 방법
        #1페이지를 출력하면 tried가 하나 올라가고, tried가 cnt(입력받은 값)보다 작을 경우까지 프로그램 동작


if __name__ == "__main__":
    word = input("무슨 단어를 검색할까요?: ")
    cnt = input("몇 페이지를 검색할까요?(한 페이지에 10개 기사): ")
    #여기서 입력받은 검색어와 페이지를 클래스 선언 시 변수로 전달해서 사용

    scraper = Scraper(word, int(cnt))
    scraper.scrap()