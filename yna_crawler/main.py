import pandas as pd
from time import sleep

# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# 직접 만든 모듈 불러오기
import soup

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://www.yna.co.kr/theme/mostviewed-date/index"
driver.get(url)

# 많이 본 뉴스의 카테고리
category = ['politics', 'economy', 'society', 'international', 'sports', 'entertainment']

# 리스트 생성
cat = []
title = []
content = []
keyword = []

# 카테고리별 반복 - 총 6부문
for word in category:
    n_sel = f'#container > div > div:nth-child(2) > div.tab-type01.tab-detail-date > ul > li.{word} > a'
    driver.find_element(By.CSS_SELECTOR, n_sel).click()
    sleep(2)

    # 상위 5개 반복 - 총 5개
    for i in range(5):
        try:
            # 이전 날짜로 타임리프
            # driver.find_element(By.CSS_SELECTOR, '#container > div > div:nth-child(2) > div.period-zone > fieldset > div.period-form01 > button.btn-dir01-prev > span').click()
            # sleep(3)

            # 많이 본 뉴스의 기준이 되는 날짜 
            std_date = driver.find_element(By.CSS_SELECTOR, '#container > div > div:nth-child(2) > div.period-zone > fieldset > div.period-form01 > strong').text

            # 첫번째 키워드 저장
            k = driver.find_element(By.CSS_SELECTOR, f'#container > div > div:nth-child(3) > section > div > ul > li:nth-child({i+1}) > div > div.news-con > ul> li:nth-child(1) > a').text
            keyword.append(k[1:])

            # 기사 진입
            driver.find_element(By.CSS_SELECTOR, f'#container > div > div:nth-child(3) > section > div > ul > li:nth-child({i+1}) > div > div.news-con > a').click()
            sleep(2)
            res = driver.current_url

            try:
                sret = soup.soupify(res)
                sleep(2)
                # 각 리스트에 추가
                cat.append(word)
                title.append(sret[0])
                content.append(sret[1])

            except:
                print("요소를 찾을 수 없음")
                cat.append(word)
                title.append('요소를 찾을 수 없음')
                content.append('요소를 찾을 수 없음')

        except:
            print(f"{word} 분야의 {i+1}번째 기사 진입실패")
            if len(keyword) == len(cat):
                keyword.append('키워드 추출실패')
            cat.append(word)
            title.append(f'{word} 분야의 {i+1}번째 기사 진입실패')
            content.append(f'{word} 분야의 {i+1}번째 기사 진입실패')

        finally:
            # 뒤로 이동
            driver.back()
            sleep(1)

# 작별을 고합니다! 수고했어 :)
driver.quit()

content = {'카테고리':cat, '기사제목':title, '전문':content, '키워드':keyword}
df = pd.DataFrame(data=content)

# !주의! 경로 직접 지정
df.to_csv(f'./crawled/{std_date}_news.csv', encoding='utf-8')