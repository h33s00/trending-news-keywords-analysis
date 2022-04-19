import requests
from bs4 import BeautifulSoup

def soupify(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    # 기사 제목
    title = soup.select("#articleWrap > div.content03 > header > h1")[0].text
    # 기사 전문
    article = soup.select("#articleWrap > div.content01.scroll-article-zone01 > div > div > article > p")[:-2]

    # 1차 전처리 작업 결과물
    cut = ''
    # 추가적인 작업 가능 여부 확인 필요!
    for index, item in enumerate(article):
        k = str(item)
        if "기자" in str(item):
            k = k[k.index("기자")+2:]    
        cut += k
    
    return title, cut

# print(soupify('https://www.yna.co.kr/view/AKR20220303160600371'))