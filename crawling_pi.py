#-*- coding: utf-8 -*-
#from urllib2 import urlopen
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import time

def ttsTime():
    result = ("지금은 " + str(time.localtime(time.time()).tm_mon) + "월 "
          + str(time.localtime(time.time()).tm_mday) + "일.. "
          + str(time.localtime(time.time()).tm_hour) + "시 ..."
          + str(time.localtime(time.time()).tm_min) + "분 "
          + "입니다....")
    print(result)
    return result

def ttsMatch():
    # GET_TIME
    year = time.localtime(time.time()).tm_year
    month = time.localtime(time.time()).tm_mon
    if int(month / 10) == 0:
        month = "0" + str(month)
    day = time.localtime(time.time()).tm_mday
    if int(day / 10) == 0:
        day = "0" + str(day)
        
    # TEST
    year = 2020; month = "06"; day = "20" ## 테스트 하려면 값 변경
    date = str(year) + str(month) + str(day)

    # WEB CRAWLING
    addr = "https://sports.news.naver.com/kbaseball/schedule/index.nhn?date=" \
         + str(date) + "&month=" + str(month) + "&year=" + str(year) + "&teamCode=SS"
    html = urlopen(addr)
    res = requests.get(addr)
    bsObject = BeautifulSoup(res.content, "html.parser")

    match_info = ""
    i = 0
    day = int(day)
    info = []

    # 모든 데이터
    for link in bsObject.find_all('tr'):
        match_info = link.text.strip()
        match_info = match_info.replace('\n', ' ')
        match_info = match_info.replace('\t', '')
        match_info = match_info.replace('   ', '')
        #print(match_info)#모든 데이터 출력

    info= [] 
    # TXT Passing & TTS
    for link in bsObject.find_all('tr'):
        if i == day:
            # print(link.text.strip(), link.get('href')
            match_info = link.text.strip()

            match_info = match_info.replace('\n', ' ')
            match_info = match_info.replace('\t', '')
            match_info = match_info.replace('   ', '')
            info.append(match_info.split(' '))

            #print(info, len(info[0]))
            if len(info[0]) >= 10:
                # 날짜
                t_m, t_d = info[0][0].split('.')

                # 요일
                info[0][1] = info[0][1].replace(')', '')
                info[0][1] = info[0][1].replace('(', '')
                info[0][1] = info[0][1] + "요일"

                # 시간
                t_m, t_d = info[0][3].split(':')

                result = info
                print(result)
                return result
                # 상대 팀

            elif len(info[0]) <= 8:
                result = ("오늘은 프로야구 경기가 없습니다.")
                print(result)
                return result
            break
        i += 1

def getMatch() :
    channel = 0

    resultMatch = ttsMatch()
    # GET FINAL_TXT
    if len(resultMatch[0]) >= 10:
        h, m = resultMatch[0][3].split(':')
        matchTime = h + "..시.." + m + "분 ..." + resultMatch[0][8] + "...." + resultMatch[0][4] + " ..의 경기가 있습니다."

        if 'SPOTV' in resultMatch[0].__str__():
            channel = "백 이십"
            if 'SPOTV2' in resultMatch[0].__str__():
                channel = "백 이십 팔"
        elif '경기취소해당' in resultMatch[0]:
            matchTime = "..오늘은 경기가 취소되었습니다..";
            channel = -1
        elif 'KBS' in resultMatch[0]:
            channel = "백 이십 일"
        elif 'SBS' in resultMatch[0]:
            channel = "백 이십 이"
        elif 'MBC' in resultMatch[0]:
            channel = "백 이십 삼"
    else:
        matchTime = resultMatch

    if channel == -1 or channel == 0:
        result_txt = "..." + matchTime
    elif channel != -1 and channel != 0:
        result_txt = "..." + matchTime + ".." + str(channel) + "번 입니다."


    return result_txt


if __name__ == "__main__" :
    print(getMatch())