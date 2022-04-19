import pandas as pd

# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://www.yna.co.kr/theme/mostviewed-date/index"
driver.get(url)
sleep(3)

# 많이 본 뉴스의 기준이 되는 날짜
std_date = driver.find_element(
    By.CSS_SELECTOR,
    "#container > div > div:nth-child(2) > div.period-zone > fieldset > div.period-form01 > strong",
).text
print(std_date)

# 많이 본 뉴스의 카테고리
category = [
    "politics",
    "economy",
    "society",
    "international",
    "sports",
    "entertainment",
]

# 리스트 생성
cat = []
title = []
body = []

# 카테고리별 반복 - 총 6부문
for word in category:
    n_url = url + f"#{word}"
    driver.get(n_url)
    sleep(1)
    # 상위 5개 반복 - 총 5개
    for i in range(5):
        try:
            # 기사 진입
            driver.find_element(
                By.CSS_SELECTOR,
                f"#container > div > div:nth-child(3) > section > div > ul > li:nth-child({i+1}) > div > div.news-con > a",
            ).click()

            try:
                # 각 리스트에 추가
                cat.append(word)
                title.append(
                    driver.find_element(
                        By.CSS_SELECTOR, "#articleWrap > div.content03 > header > h1"
                    ).text
                )
                body.append(
                    driver.find_element(
                        By.CSS_SELECTOR,
                        "#articleWrap > div.content01.scroll-article-zone01 > div > div > article",
                    ).text
                )

            except:
                print("요소를 찾을 수 없음")

        except:
            print(f"{i+1}번째 기사 진입실패")

        finally:
            # 뒤로 이동
            driver.back()
            sleep(1)

# 작별을 고합니다! 수고했어 :)
driver.quit()

content = {"카테고리": cat, "기사제목": title, "기사전문": body}
print(content)
print(type(content))
print(type(body[1]))
df = pd.DataFrame(data=content)
df.to_csv(f"{std_date}_news.csv", encoding="cp949")
