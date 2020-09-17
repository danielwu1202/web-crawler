# 點擊show more 還有 抓多少計畫

from selenium import webdriver
from bs4 import BeautifulSoup
import random
import time
import csv

url = 'https://www.indiegogo.com/explore/energy-green-tech?project_type=campaign&project_timing=all&sort=trending'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
driver = webdriver.Chrome(r'C:\Users\USER\Desktop\python\Side Project\pysql\python-selenium\chromedriver.exe')
driver.get(url)

c = driver.find_element_by_link_text('SHOW MORE')

num_click = 0

while num_click < 5:
    c.click()
    num_click += 1

# 發出網路請求後讓網頁內容載入完成
time.sleep(random.randint(10, 60))

page_content = driver.page_source

soup = BeautifulSoup(page_content, 'html.parser')
# 選取時應該把 class name 為 exploreDetail-campaigns 下的所有 超連結 a 取出，才會變成可以迭代的多個 BeautifulSoup 物件，不然就只會有一個最外圍的 div
elements = soup.select('.exploreDetail-campaigns a')
# print(elements)
url_list = []

# 一一取出超連結元素 BeautifulSoup 物件
for element in elements:
    print(element.attrs)
    data = {}
    # 使用 BeautifulSoup 的 attrs 取出物件屬性
    data['project_url'] = element.attrs['href']
    url_list.append(data)    

headers = ['project_url']

# 使用檔案 with ... open 開啟 write (w) 寫入檔案模式，透過 csv 模組將資料寫入
with open('indiegogo_url_green_tech.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, headers)
    # 寫入標題
    dict_writer.writeheader()
    # 寫入值
    dict_writer.writerows(url_list)

# 使用 with ... open 開啟讀取 read (r) 檔案模式，透過 csv 模組將已經存成檔案的資料讀入
with open('indiegogo_url_green_tech.csv', 'r', newline='', encoding='utf-8') as input_file:
    rows = csv.reader(input_file)
    # 以迴圈輸出每一列，每一列是一個 list
    for row in rows:
        print(row)
driver.quit()
