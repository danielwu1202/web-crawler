from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

url = 'https://www.indiegogo.com/explore/energy-green-tech?project_type=campaign&project_timing=all&sort=trending'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}

driver = webdriver.Chrome(r'C:\Users\USER\Desktop\python\Side Project\pysql\python-selenium\chromedriver.exe')
driver.get(url)
page_content = driver.page_source
soup = BeautifulSoup(page_content, 'html.parser')

elements = soup.find('section', 'exploreResults')
print(elements)
url_list = []

for element in elements:
    project_url = element.select('a .href')
    data = {}
    data['project_url'] = project_url.text
    url_list.append(data)

time.sleep(10)
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