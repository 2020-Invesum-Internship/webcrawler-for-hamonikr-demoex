import itertools

import requests
import pandas as pd
from bs4 import BeautifulSoup
# url 뒤에 붙을 숫자 범위
ran = range(1, 11071)
url = "https://hashcode.co.kr/questions/"
# url 뒤에 지정한 범위 내의 숫자를 붙여 배열에 저장
url_list = []
for r in ran:
    url_list.append(url + str(r))
data_list = []
for url in url_list:
    # 진행 상황 파악하기 위해 링크 출력
    print(url)
    # 파싱 작업
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    #제목 추출
    title = soup.select('body > div.main > div.content > div.content-wrap > div.center > h2 > a')
    #본문 추출
    contents = soup.select(
        'body > div.main > div.content > div.content-wrap > div.center > div.content.question-body > div.markdown')
    #답변 추출 (답변과 그의 댓글을 함께 추출한다)
    answers = soup.select(
        'ul.answers-list > li.answer-item > div.center')


    list=[]
    # 답변이 존재할 경우
    if answers:
        # 배열 형태인 답변들을 text 형으로 전환
        for answer in answers:
            # 답변 본문 추출
            answer_markdown=answer.find_all(attrs={'class':'markdown'})
            # 답변의 댓글 추출
            answer_comment=answer.find_all(attrs={'class':'comment-content'})
            # list에 답변 본문 삽입
            list.append(answer_markdown[0].text)
            # list에 댓글 구분자 삽입
            list.append("\n\n<---------댓글----------->\n")
            # list에 댓글 삽입
            for ans in answer_comment:
                list.append(ans.text)

            # 각 답변을 구분하는 구분자 삽입
            list.append('\n*************************************************************\n')

        # 모든 답변, 댓글 사이의 간격 삽입, 리스트 합치기
        answer_str = "\n\n".join(list)

    # 답변이 존재하지 않을 경우 예외 처리
    if not answers:
        answer_str = "No Answers Exist"

    # 태그 추출
    tag = soup.select(
        'body > div.main > div.content > div.content-wrap > div.center > div.question-tags')
    if not tag :
        tag = "No Tags Exist"
    # 추출한 데이터 삽입
    for item in zip(title, contents, answer_str, tag):
        data_list.append(
            {
                '제목': item[0].text,
                '내용': item[1].text,
                '답변': answer_str,
                '태그': item[3].text.replace('\n', '').replace('\t', '').replace('  ', '')
            }
        )
# 추출한 데이터 csv파일 형태로 저장
data = pd.DataFrame(data_list)
data.to_csv('crawling_hashcode.csv')