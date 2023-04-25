from selenium import webdriver
from selenium . webdriver . chrome .service import Service
from selenium . webdriver . common. keys import Keys
from selenium . webdriver . common. by import By
import os
from selenium.webdriver.support.wait import WebDriverWait
driver= webdriver.Chrome('/home/fish/Documents/WebScraping/driver/chromedriver_ubuntu119')
driver. get (target[1])


title = driver.find_element(By.XPATH, '/html/body/div[3]/main/div/div/article/div/div[2]/h1').text
time = driver.find_element(By.XPATH, '/html/body/div[3]/main/div/div/article/div/div[3]/div[1]/div[1]/time').text
abs1 = driver.find_element(By.XPATH, '/html/body/div[3]/main/div/div/article/div/div[2]/ul/li[1]').text
abs2 =  driver.find_element(By.XPATH, '/html/body/div[3]/main/div/div/article/div/div[2]/ul/li[2]').text
para1 = driver.find_element(By.XPATH, '/html/body/div[3]/main/div/div/article/div/div[3]/div[2]/div/div/p[1]').text
para2 =  = driver.find_element(By.XPATH, '/html/body/div[3]/main/div/div/article/div/div[3]/div[2]/div/div/p[2]').text
