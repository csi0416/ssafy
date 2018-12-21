# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request
import requests

from random import *
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template
from urllib import parse

app = Flask(__name__)

slack_token = ""
slack_client_id = ""
slack_client_secret = ""
slack_verification = ""
sc = SlackClient(slack_token)

dic ={}

chan="#day4"

# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    list = text.split(" ")
    st=""
    for i, item in enumerate(list):
        if i>0 :
            st+=item

    print(st)
    if "안녕" in st:
        sc.api_call(
            "chat.postMessage",
            channel=chan,
            text="안녕하세요"
        )
    if "몇살" in st:
        sc.api_call(
            "chat.postMessage",
            channel=chan,
            text="26살입니다"
        )

    if "코인" in st:
        names =[]

        soup = BeautifulSoup(urllib.request.urlopen('https://coinmarketcap.com/').read(), 'html.parser')

        for i, keyword in enumerate(soup.find_all("a", class_="currency-name-container link-secondary")):
            if(i<10):
                names.append(keyword.get_text())
        for i, keyword in enumerate(soup.find_all("a", class_="price")):
            if (i < 10):
                names[i]+=" "+ keyword.get_text()

        sc.api_call(
            "chat.postMessage",
            channel=chan,
            text=u'\n'.join(names)+"\nhttps://coinmarketcap.com/"
        )
    # if "구글링" in st:
    #     word = parse.quote(list[1])
    #     #print(word)
    #     headers = {'User-Agent': 'Mozilla/5.0'}
    #     URL = "https://www.google.com/search?q="+word
    #     soup = BeautifulSoup(urllib.request.Request(URL, None, headers))
    #
    #     for key in soup.find_all("div", class_="y8AWGd llvJ5e"):
    #         img = key.find("a")["href"]
    #         print(img)



    if "동영상" in st:
        if "검색" in st:
            i = randint(1, 5)
            word = parse.quote(list[1])
            req = urllib.request.Request('https://www.youtube.com/results?search_query='+word, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
            print(word)
            response = urllib.request.urlopen(req).read()
            soup = BeautifulSoup(response, 'html.parser')
            print(soup)

            for j, key in enumerate(soup.find_all("h3", class_="yt-lockup-title ")):
                if j==i:
                    sc.api_call(
                        "chat.postMessage",
                        channel='chan',
                        text="https://www.youtube.com" + key.find("a")["href"]
                    )
                    break


            # #링크한줄 추천
            # req = urllib.request.Request('https://www.youtube.com',headers={'User-Agent': 'Mozilla/5.0'})
            # response = urllib.request.urlopen(req).read()
            # soup = BeautifulSoup(response, 'html.parser')
            #
            # for key in soup.find_all("ol", class_="item-section"):
            #
            #     sc.api_call(
            #         "chat.postMessage",
            #         channel='#general',
            #         text="https://www.youtube.com"+key.find("a")["href"]
            #     )
            #     break



            #for key in soup.find_all("a", class_="yt-simple-endpoint inline-block style-scope ytd-thumbnail"):
             #   print(key.find("yt-img-shadow")["src"])
              #  keywords.append(key.find("yt-img-shadow")["src"])

            # sc.api_call(
            #     "chat.postMessage",
            #     channel='#general',
            #     text=keywords
            # )

        if "노래" in st:
            keywords=[]
            soup = BeautifulSoup(urllib.request.urlopen('https://music.bugs.co.kr').read(),'html.parser')
            for i, keyword in enumerate(soup.find_all("p", class_="title")):
                if (9 < i <= 20):
                    keywords.append(str(i - 9) + "위:" + keyword.get_text().strip())
            sc.api_call(
                "chat.postMessage",
                channel='chan',
                text="벅스 인기차트\n"+u'\n'.join(keywords)+"\nhttps://music.bugs.co.kr"
            )
        elif "게임" in st:
            keywords = []
            soup = BeautifulSoup(urllib.request.urlopen('https://store.steampowered.com/').read(), 'html.parser')
            for i, keyword in enumerate(soup.find_all("div", class_="tab_item_name")):
                if (i <= 10):
                    if i==0:
                        keywords.append(str(i+1) + "st:" + keyword.get_text().strip())
                    elif i==1:
                        keywords.append(str(i + 1) + "nd:" + keyword.get_text().strip())
                    elif i==2:
                        keywords.append(str(i + 1) + "rd:" + keyword.get_text().strip())
                    else :
                        keywords.append(str(i + 1) + "th:" + keyword.get_text().strip())
            sc.api_call(
                "chat.postMessage",
                channel='chan',
                text="Steam New and Trending\n" + u'\n'.join(keywords)+"\nhttps://store.steampowered.com/"
            )

    if "끝말" in st:

        sc.api_call(
            "chat.postMessage",
            channel='chan',
            text="먼저 시작할게, 거북이"
        )


    # if "+" in list[1]:
    #     nums = list[1].split("+")
    #     sum=int(nums[0])+int(nums[1])
    #     print(sum[0])
    #     print(sum[1])
    #     print(sum[2])
    #     sc.api_call(
    #         "chat.postMessage",
    #         channel='#general',
    #         text=""+sum
    #     )



    # home = "www.google.com"
    keywords=[]
    # # # 여기에 함수를 구현해봅시다.
    # url = re.search(r'(https?://\S+)', text.split('|')[0]).group(0)
    # url+="search?q="+list[1]
    # req = urllib.request.Request(url)
    # sourcecode = urllib.request.urlopen(url).read()
    # soup = BeautifulSoup(sourcecode, "html.parser")
    # image = soup.find("img")["src"]
    # print(image)

    # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
    return u'\n'.join(keywords)


# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        keywords = _crawl_naver_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=5000)
