# pip install konlpy
# konlpy 공식 문서에서 설치방법 참고!

from konlpy.tag import Komoran
from konlpy.utils import pprint
from collections import Counter

import pandas as pd

# CSV 파일을 지정하여 불러옵니다.
df = pd.read_csv("../crawled/2022.03.11_news.csv")
komoran = Komoran()
print(df.head())
title = df["기사제목"]
body = df["전문"]

# Most Frequent Keyword Extractor
# 아주 심플한 로직: 가장 빈도수 높은 키워드 순으로 정렬합니다.
def find_mfkeyword(doc):
    nouns = komoran.nouns(doc)
    # 정확도 향상을 위해 한글자 단어 없애기
    new_nouns = []
    for word in nouns:
        if len(word) > 1:
            new_nouns.append(word)
    # print(new_nouns)
    sorted_nouns = sorted(new_nouns, key=Counter(new_nouns).get, reverse=True)
    print("정리된 리스트", sorted_nouns, "끝")
    # 가장 자주 출현한 키워드 TOP3
    top = [sorted_nouns[0]]
    for item in sorted_nouns:
        if top[-1] != item:
            top.append(item)
    top_three = top[:3]
    hashtop = f"#{top[0]}_{top[1]}_{top[2]}"
    return hashtop


print(find_mfkeyword(body[6]))

# for item in body:
#     print(find_mfkeyword(item))
