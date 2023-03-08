# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 12:35:17 2023

@author: blithe
"""

import praw
import csv
from datetime import datetime, timedelta

# Set up a Reddit instance
reddit = praw.Reddit(client_id='VM9jFKD9OstAHXBHYraPHQ',
                     client_secret='cyzA9Bugc1tQzIh8IBIoD8xe87hCPw',
                     user_agent='blithedou')

keyword = input("Please input the keyword：")

#time filter can only choose recent day, week, month, year
search_results = reddit.subreddit('all').search(keyword,sort='new', time_filter='year')
csv_data = []

# Get the current time and calculate the time threshold so that can choose eg 60 days
current_time = datetime.utcnow()
time_threshold = current_time - timedelta(days = 60)

# 遍历搜索结果
for post in search_results:
   # if datetime.utcfromtimestamp(post.created_utc) >= time_threshold:
        post_data = [post.title, post.url]
        if 'reddit' not in post.url:
            continue
        if not post.comments:
            post_data.append('')
        else:
            comment = post.comments[0].body
            post_data.append(comment)
        csv_data.append(post_data)

# 将 CSV 数据写入文件
with open('reddit_data.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'URL', 'Comment'])
    writer.writerows(csv_data)

