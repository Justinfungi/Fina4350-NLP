# coding gbk
# -*-utf-8-*-
# bloomberg

from time import sleep
import requests
# from fake_useragent import UserAgent
import pandas as pd
import json


def main():
    startPage = int(input("请输入起始页数："))
    url = f'https://www.bloomberg.com/markets2/api/search?query=amazon&page={str(startPage)}&sort=time:desc'
    res = requests.get(url=url, headers=headers, proxies=proxies).text
    data = json.loads(res)
    print(data)
    totalPage = int(data['total'] / 10)
    for p in range(startPage, totalPage + 1):
        url = f'https://www.bloomberg.com/markets2/api/search?query=amazon&page={str(p)}&sort=time:desc'
        res = requests.get(url=url, headers=headers, proxies=proxies).text
        data = json.loads(res)
        print(data)
        for item in data['results']:
            title = item['headline']
            date = item['publishedAt']
            summary = item['summary']
            detailLink = item['url']
            authors = item['authors']
            dic = {
                'title': title,
                'date': date,
                'summary': summary,
                'detailLink': detailLink,
                'authors': authors,
            }
            print(dic)
            resL.append(dic)
        df = pd.DataFrame(resL)
        df.to_csv('bloomberg.csv', index=False, encoding='utf-8')
        print('已爬' + str(p) + '页')


if __name__ == '__main__':
    resL = []
    # 代理ip
    proxy = '127.0.0.1:7890'
    proxies = {
        'http': 'http://' + proxy,
        'https': 'http://' + proxy
    }
    # ua = UserAgent(path=r"D:\Pychram\pc\MyProject\fake_useragent.json")
    headers = {
        # 'user-agent': ua.random,
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'agent_id=d68d5043-dd1f-4cc6-bfce-8c9f18fd041d; session_id=25e915ad-db9e-4e26-84ce-88dcfc8d1493; session_key=3dc713066ac33009cf9db8728582dad2918f5052; gatehouse_id=25593486-26f5-4abc-9ee2-1f4f2ed52998; geo_info=%7B%22countryCode%22%3A%22HK%22%2C%22country%22%3A%22HK%22%2C%22field_n%22%3A%22cp%22%2C%22trackingRegion%22%3A%22Asia%22%2C%22cacheExpiredTime%22%3A1682155507998%2C%22region%22%3A%22Asia%22%2C%22fieldN%22%3A%22cp%22%7D%7C1682155507998; _pxvid=69bdf69c-db6f-11ed-ac18-45436a6a4b59; geo_info={%22country%22:%22HK%22%2C%22region%22:%22Asia%22%2C%22fieldN%22:%22cp%22}|1682155508996; _sp_krux=false; _sp_v1_ss=1:H4sIAAAAAAAAAItWqo5RKimOUbLKK83J0YlRSkVil4AlqmtrlXRGlQ0dZbEAf3mLbNUBAAA%3D; _sp_su=false; ccpaUUID=33059519-4cff-4a43-b9e6-a7887d0bf477; dnsDisplayed=true; ccpaApplies=true; signedLspa=false; bbgconsentstring=req1fun1pad1; _gcl_au=1.1.1082629904.1681550710; bdfpc=004.1933831791.1681550710261; _fbp=fb.1.1681550711670.1863016116; _rdt_uuid=1681550711833.c7c8ffe6-6e2c-4b0d-b637-0d1536391a74; _scid=d84c3c24-eee1-4404-bb30-7534e15056ec; _cc_id=6b0651dbfbe706659a4d496aca234c11; _lc2_fpi=b1166d620485--01gy23qajxz31pkg4a75cw9mrx; _sctr=1%7C1681488000000; optimizelyEndUserId=oeu1681550727229r0.014651223888104914; _sp_v1_uid=1:449:2eb1275c-1e40-4b96-b4ca-6d3b4c4b8b26; exp_pref=AMER; _gid=GA1.2.1929169323.1681701296; seen_uk=1; _reg-csrf-token=BlihgHS3-smHjYeL5ERXaACNfZeSBidIdIvg; _reg-csrf=s%3As-rNTQ3NoEx9NJmuyhDsvUwd.wUO5%2BOmxpsMfhhiZ19Fq0xjOVMcc7sWdM8tMR4KYYDk; _user-data=%7B%22status%22%3A%22anonymous%22%7D; _last-refresh=2023-4-17%203%3A15; pxcts=163419f7-dcce-11ed-8b8c-69716d436e4b; _sp_v1_data=2:585912:1678069814:0:25:0:25:0:0:_:-1; _ga=GA1.2.1090712087.1681550710; __sppvid=7fa0c939-c929-4c23-b613-ef7bbd0ee06a; _uetsid=1739acf0dcce11ed81f0f15b32b3b87a; _uetvid=6baf7d30db6f11ed80995d510eec43c3; _scid_r=d84c3c24-eee1-4404-bb30-7534e15056ec; _px3=7b757eb35bbdc9629e17cf3ef8ecba13132256e973d74b4e5ca679ec72b07550:YiEGi3hoWaOvaHi0m+/jDYYwlaDzlYCrvp9d+N8xhyK1yoLnTeI6HjNvcO2nAOdxM4zvIwCypX4a1dlAd46G9A==:1000:aFAJR8TMqqD8IuyuzTOEANWXy089OP7T8gODArnt9qWYd/QVuSicloDeJYic+F41OXpIq1W0U6VMjOZdNinCJb/duaDkCjRFNGWM/mgPLRyac136LzggeBEOdOTNJqLXgJEGf4bC10mQlzqvNk2C8TYuYDA+P34rdDdBTBnepzAWeQC7jhtBEnLEdDvwHgwdIPQu7eui9NYT+FJolBjJ5g==; _px2=eyJ1IjoiMTU4YWUwMzAtZGNjZS0xMWVkLTk5ZDEtMmZlOGNhNGIyMGM5IiwidiI6IjY5YmRmNjljLWRiNmYtMTFlZC1hYzE4LTQ1NDM2YTZhNGI1OSIsInQiOjE2ODE3MDE2MjM1MzYsImgiOiJkNWY0YWFhZGEyNzYyODhlMmRjNjBlMDdlZmI5NDc0YmE5YWFmNDY5Zjc2NDJmZDMxZjc3MWI1NDhmYjVhMjZiIn0=; ln_or=eyI0MDM1OTMiOiJkIn0%3D; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://www.bloomberg.com/search?query=amazon%22%2C%22sref%22:%22https://www.bloomberg.com/asia%22%2C%22sts%22:1681701324247%2C%22slts%22:1681550713255}; _parsely_visitor={%22id%22:%22pid=5ade70daa872a324a8f9b9c00a9bbd45%22%2C%22session_count%22:2%2C%22last_session_ts%22:1681701324247}; _li_dcdm_c=.bloomberg.com; panoramaId_expiry=1681787725795; panoramaId=8ec962754d7264e8bddf4b1e3dc4a9fb927a0018a5e1ca7c32dd6b5ac042a673; panoramaIdType=panoDevice; _pxde=b9d87a2a49307f1bd27ba7d2f3096773cbaf4f3bc90e6d72286202171048e81a:eyJ0aW1lc3RhbXAiOjE2ODE3MDEzNDI4NDgsImZfa2IiOjAsImlwY19pZCI6W119; _gat_UA-11413116-1=1; _ga_GQ1PBLXZCT=GS1.1.1681701295.2.1.1681701367.0.0.0',
        'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjE5ODI2OTciLCJhcCI6IjE0MDk1Mjc5OCIsImlkIjoiZDk0NmVmYzBhYjAwZWFiYSIsInRyIjoiOGE1MjQ1YWQ3MTAyMDJlMDMyNzBlMTNjZWVhZTdiODAiLCJ0aSI6MTY4MTcwMTM2NzI4NSwidGsiOiIyNTMwMCJ9fQ==',
        'referer': 'https://www.bloomberg.com/search?query=amazon',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'traceparent': '00-8a5245ad710202e03270e13ceeae7b80-d946efc0ab00eaba-01',
        'tracestate': '25300@nr=0-1-1982697-140952798-d946efc0ab00eaba----1681701367285',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    main()
