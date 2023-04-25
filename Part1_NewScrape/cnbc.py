# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 23:05:07 2023

@author: blithe
"""

from time import sleep
import requests
# from fake_useragent import UserAgent
import pandas as pd
from bs4 import BeautifulSoup


def main():
    keyword = input("请输入关键词：")
    endindex = 0
    while 1:
        url = f'https://api.queryly.com/cnbc/json.aspx?queryly_key=31a35d40a9a64ab3&query={keyword}&endindex={str(endindex)}&batchsize=10&callback=&showfaceted=false&timezoneoffset=-480&facetedfields=formats&facetedkey=formats|&facetedvalue=!Press Release|&additionalindexes=4cd6f71fbf22424d,937d600b0d0d4e23,3bfbe40caee7443e,626fdfcd96444f28 '
        res = requests.get(url=url, headers=headers).json()
        data = res['results']
        for item in data:
            title = item['cn:title']
            date = item['_pubDate']
            summary = item['description']
            link = item['url']
            section = item['section']
        #    print(link)
            resp = requests.get(url=link, headers=headers).text
            soup = BeautifulSoup(resp, 'lxml')
            try:
                result=''
                # text = soup.find('div',class_='ArticleBody-articleBody').find('div',class_='group').text
                first_group = soup.select_one('.ArticleBody-articleBody > div.group')
                text = [first_group] + first_group.find_next_siblings()
                for elem in text:
                    result += elem.text.strip()
              #  print(result)
            except:
                result = ''
            # print(resp)
            if soup.find('div', class_='RenderKeyPoints-list') is None:
                summary_ = summary
            else:
                content_li = soup.find('div', class_='group').find('ul').find_all('li')
                # print(content_li)
                content = ''
                for li in content_li:
                    content += li.text
                summary_ = content
              #  print('摘要：' + summary_)
            dic = {
                'title': title,
                'date': date,
                'link': link,
                'section': section,
                'summary': summary_,
                'content': result
            }
        #    print(dic)
            resL.append(dic)
        df = pd.DataFrame(resL)
        writer = pd.ExcelWriter(f'{keyword}_cnbc.xlsx')
        df.to_excel(writer, index=False, encoding='utf-8')
        writer.save()
        print('已爬' + str(res['metadata']['pagerequested']) + '页')
        # print(int(res['metadata']['totalresults']))
        if endindex > int(res['metadata']['totalresults']):
            break
        else:
            endindex += 10


if __name__ == '__main__':
    resL = []
    # ua = UserAgent(path=r"D:\Pychram\pc\MyProject\fake_useragent.json")
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        # ua.random,
    }
    main()
