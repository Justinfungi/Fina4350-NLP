# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 18:09:53 2023

@author: blithe
"""

import twint
import nest_asyncio
import pandas as pd
import chardet
nest_asyncio.apply()

keyword = input("请输入要搜索的关键词：")
c = twint.Config()

c.Search = keyword
c.Store_csv = True
c.Lang = 'en'
c.Count = True
c.Since = '2023-03-24'
c.Output = f"{keyword}.csv"
c.Pandas = True
c.Pandas_clean = True
c.Lowercase = True
c.Hide_output = True
c.Pandas_au = True

twint.run.Search(c)

"""
编码问题不好程序改
notepad++打开后，编码先转ANSI，再转UTF-8，另存为。
google作为关键词存的，但是google本身是个动词感觉这样参考意义不大
"""