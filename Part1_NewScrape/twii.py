# coding gbk
# -*-utf-8-*-
# 推特


import os
import random
import re
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
# import undetected_chromedriver as uc
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver import Chrome, Keys
import winsound


def main():
    cnt = 0
    driver.get(url)
    input('刷新完成输入enter:')
    time.sleep(2)
    div_list = driver.find_elements(By.XPATH,
                                    '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/section/div/div/div')
    for div in div_list:
        try:
            content = div.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
        except Exception as e:
            print(e)
            continue
        if content.get_attribute('id') in content_l:
            continue
        print(content.text)
        try:
            time_element = div.find_element(By.XPATH, './/time').text
        except Exception as e:
            print(e)
            continue
        # 找到包含链接的<div>元素
        link_div = div.find_element(By.XPATH, './/div[@class="css-1dbjc4n r-18u37iz r-1q142lx"]')
        # 找到链接所在的<a>元素
        link_element = link_div.find_element(By.XPATH, './/a').get_attribute('href')
        content_l.append(content.get_attribute('id'))
        dic = {
            '内容': content.text,
            '时间': time_element,
            '链接': link_element
        }
        print(dic)
        resL.append(dic)
    old_scroll_height = 0  # 表明页面在最上端
    js1 = 'return document.body.scrollHeight'  # 获取页面高度的javascript语句
    js2 = 'window.scrollTo(0, document.body.scrollHeight)'  # 将页面下拉的Javascript语句
    actions = ActionChains(driver)
    while driver.execute_script(js1) > old_scroll_height:  # compare the height
        div_list = driver.find_elements(By.XPATH,
                                        '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/section/div/div/div')
        for div in div_list:
            try:
                content = div.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
            except Exception as e:
                print(e)
                continue
            if content.get_attribute('id') in content_l:
                continue
            cnt += 1
            print(content.text)
            try:
                time_element = div.find_element(By.XPATH, './/time').text
            except Exception as e:
                print(e)
                continue
            link_div = div.find_element(By.XPATH, './/div[@class="css-1dbjc4n r-18u37iz r-1q142lx"]')
            link_element = link_div.find_element(By.XPATH, './/a').get_attribute('href')
            content_l.append(content.get_attribute('id'))
            dic = {
                'Content': content.text,
                'Time': time_element,
                'Link': link_element
            }
            print(dic)
            resL.append(dic)
            df = pd.DataFrame(resL)
            writer = pd.ExcelWriter(f'{key}_twi.xlsx')
            df.to_excel(writer, index=False, encoding='utf-8')
            writer.save()
        old_scroll_height = driver.execute_script(js1)  # get current height
        driver.execute_script(js2)  # pull the weber
        for j in range(5):
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1)
        time.sleep(4)  #leave load time
        if (driver.execute_script(js1) <= old_scroll_height): # deal with the crush of web pages
            cnt = 0
            winsound.Beep(3000, 3000) #sound alert
            input('Enter:')
            old_scroll_height = 0  # 
            js1 = 'return document.body.scrollHeight'  

    input('请输入enter:')
    driver.quit()


if __name__ == '__main__':
    resL = []
    content_l = []
    key = input('请输入关键词：')
    url = f'https://twitter.com/search?q={key}%20lang%3Aen%20until%3A2023-04-07%20since%3A2023-01-01&src=typed_query&f=live'  # &f=live
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images1": 2,
             "profile.managed_default_content_settings.javascript": 1,
             'permissions.default.stylesheet': 2}
    options.add_experimental_option("prefs", prefs)
    # options.add_argument('--headless')
    # options.add_argument(
    #     'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #     'Chrome/94.0.4606.71 Safari/537.36')
    driver = Chrome(options=options)
    driver.implicitly_wait(10)
    with open('stealth.min.js') as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })

    main()
