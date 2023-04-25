# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 17:53:28 2023

@author: blithe
"""

import re
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup


def main():
    p = 1
    pageNum = 0
    while 1:
        url = f'https://www.wsj.com/search?query={keyword}&mod=searchresults_viewallresults&page={str(p)}'
        browser.get(url)
        sleep(1)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        if p == 1:
            pagenum = soup.find('span', class_='WSJTheme--total-pages--3FkCtMxZ').text
            pageNum = re.search(r"\d+", pagenum).group()
            print('总页数：' + str(pageNum))
        div_list = soup.find_all('div', class_='WSJTheme--search-text-combined--29JN8aap')
        print(div_list)
        for div in div_list:
            title = div.find('span').text
            link = div.find('a').get('href')
            try:
                date = div.find('p', class_='WSJTheme--timestamp--22sfkNDv').text
            except:
                date = ''
            try:
                summary = div.find('span', class_='WSJTheme--summaryText--2LRaCWgJ').text
            except:
                summary = ''
            dic = {
                'title': title,
                'date': date,
                'link': link,
                'summary': summary
            }
            print(dic)
            resL.append(dic)
        df = pd.DataFrame(resL)
        writer = pd.ExcelWriter(f'{keyword}_wsj.xlsx')
        df.to_excel(writer, index=False, encoding='utf-8')
        writer.save()
        print('已爬' + str(p) + '页')
        if p == int(pageNum):
            break
        else:
            p += 1
        sleep(1)


if __name__ == '__main__':
    resL = []
    keyword = input("请输入关键词：")
    options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images1": 2,
    #          "profile.managed_default_content_settings.javascript": 1,
    #          'permissions.default.stylesheet': 2}
    # options.add_experimental_option("prefs", prefs)
    options.add_argument('--headless')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/94.0.4606.71 Safari/537.36')
    browser = Chrome(options=options)
    browser.implicitly_wait(10)
    with open('stealth.min.js') as f:
        js = f.read()
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    main()
