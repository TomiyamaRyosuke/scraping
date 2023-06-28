#%%
from time import sleep
from retry import retry
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import os
 
 # 室蘭市のアパマンショップのリンク
base_url = "https://www.chintaistyle.jp/pref/01/area_12293_list.html?page={}&disp=10&item=aprm&ar=asc"

@retry(tries=3, delay=5, backoff=2)
def get_html(target_url):
     r = requests.get(target_url)
     soup = BeautifulSoup(r.content, "html.parser")
     return soup

 #データの格納場所
all_data = []
 #複数ページの情報を取得する
max_page = 20
for i in range(0,max_page):
     target_url = base_url.format(i)
     soup =  get_html(target_url)
    
     items = soup.find_all("form", {"action": "/lib/manage_mylist.html"})
    
     for item in items:
         lists = soup.find_all("a", {"class": "ListTableA"})
    

     # listsの中から指定した情報を抜き出す
         for list in lists:

             base_data = {} 
             base_data["物件名"] = list.find("h2", {"class": "estate-parent-rightTopTD_P2 alignLEFT"}).getText().strip()
             base_data["エリア"] = list.find("li", {"class": "estate-parent-rightBottomUL1_LI1"}).getText().strip()
             base_data["エリア"] = base_data["エリア"].replace('室蘭市','') #室蘭市を削除
             base_data["最寄り駅"] = list.find("li", {"class": "estate-parent-rightBottomUL1_LI2"}).getText().strip()
             base_data["築年数"] = list.find("li", {"class": "estate-parent-rightBottomUL1_LI3"}).getText().strip()
             base_data["築年数"] = base_data["築年数"][13:] #（築〇年）のみ抽出
             base_data["築年数"] = base_data["築年数"].replace('年）','') #年）を削除
             base_data["階数"] = list.find("li", {"class": "estate-parent-rightBottomUL1_LI4"}).getText().strip()
             base_data["階数"] = base_data["階数"][5:] #階数のみ抽出
             base_data["URL"] = "https://www.chintaistyle.jp"+ list.get("href")
             all_data.append(base_data)
       

df = pd.DataFrame(all_data)

 #Excelに書き出す
df.to_excel("muroran_data.xlsx")

# %%
