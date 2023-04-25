import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
from urllib import request
import re
import pandas as pd
import numpy as np


filename = "Search - Bloomberg.html"
with open(filename,'r') as html_file:
    local = html_file.read()

s = bs(local,'lxml')
link = s.find_all("a",attrs={"class":"thumbnailWrapper__23c201ad78"})
target = []
for i in link:
    target.append(i["href"])
    print(i["href"])



pd.DataFrame(target).to_csv(f'{filename}.csv')
