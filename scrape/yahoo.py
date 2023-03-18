# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 12:52:34 2023

@author: blithe
"""
import requests
import re
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime, timedelta

keyword = input("请输入您要搜索的关键词：")
start_number = 1
articles = []

headers = {
'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9',
'referer': 'https://www.google.com',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
}


while (start_number <= 1000):
    url = f"https://news.search.yahoo.com/search?p={keyword}&b={start_number}"
    time.sleep(3)
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.content, "html.parser")
    for article in soup.find_all("div", class_="NewsArticle"):
        title = article.find("h4", class_="s-title").text.strip()
        raw_link = article.find('a').get('href')
        unquoted_link = requests.utils.unquote(raw_link)
        pattern = re.compile(r'RU=(.+)\/RK')
        link = re.search(pattern,unquoted_link).group(1)
#        link = article.find('a').get('href')
        desc = article.find('p','s-desc').text.strip()
        relative_time = article.find('span','s-time').text.strip()[2:]
        if 'hour' in relative_time:
            hours = int(relative_time.split()[0])
            date = (datetime.utcnow() - timedelta(hours=hours)).strftime("%Y%m%d")
        else:
            days = int(relative_time.split()[0])
            date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y%m%d")
        source = article.find('span','s-source').text
        articles.append([title, source, link, desc, date])

    start_number += 10  # 每次加10
    print(start_number)
    if not soup.find_all("div", class_="NewsArticle"):
        break  # 没有更多结果时停止翻页

with open(f"{keyword}_yahoo_news.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Source", "Link", "Description", "Date"])
    writer.writerows(articles)

print(f"关键词为'{keyword}'的文章已保存至{keyword}_yahoo_news.csv文件中。")