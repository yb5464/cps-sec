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

        self.writeCSV(newsTitle, newsLink, newsSource)
        
    def writeCSV(self, newsTitle, newsLink, newsSource):
        file = open('news.csv','a', newline='')
        line = csv.writer(file)

        for i in range(len(newsTitle)):
            line.writerow([str(i + 1 + self.tried * 10), newsTitle[i], newsSource[i], newsLink[i]])
        
        file.close()

    def scrap(self):

        file = open('news.csv','w', newline='')
        line = csv.writer(file)
        line.writerow(["No", "Title","Source", "Link"])
        file.close()

        while self.tried < self.cnt:
            soup = self.getHTML(self.tried)
            self.getNews(soup)
            self.tried += 1


if __name__ == "__main__":
    word = input("무슨 단어를 검색할까요?: ")
    cnt = input("몇 페이지를 검색할까요?(한 페이지에 10개 기사): ")

    scraper = Scraper(word, int(cnt))
    scraper.scrap()