import csv
import time
import requests
from bs4 import BeautifulSoup

url = 'https://www.kickstarter.com/projects/quelltech/quell-real-gaming-real-exercise-zero-compromise?ref=discovery_category'

r = requests.get(url)
resp = r.content
soup = BeautifulSoup(resp, 'lxml')
row_list = []

elements = soup.select('#main_content') 


for element in elements:
    project_name = element.find('h2', 'type-28 type-24-md soft-black mb1 project-name')
    description = element.find('p', 'type-14 type-18-md soft-black project-description mb1')
    num_backer = element.find('div', 'block type-16 type-28-md bold dark-grey-500')
    money = element.find('span', 'ksr-green-500')
    goal = element.find('span', 'money')
    location = element.find_all('span', 'ml1')
    background = element.find('span', 'bold')
    data = {}
    data['project_name'] = project_name.text
    data['description'] = description.text
    data['num_backer'] = num_backer.text
    data['money'] = money.text
    data['goal'] = goal.text
    data['category'] = location[1].text
    data['location'] = location[2].text
    data['background'] = background.text
    row_list.append(data)

time.sleep(10)
headers = ['project_name', 'description', 'num_backer', 'money', 'goal', 'category', 'location', 'background']
# 使用檔案 with ... open 開啟 write (w) 寫入檔案模式，透過 csv 模組將資料寫入
with open('kickstarter_test_2.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, headers)
    # 寫入標題
    dict_writer.writeheader()
    # 寫入值
    dict_writer.writerows(row_list)
# 使用 with ... open 開啟讀取 read (r) 檔案模式，透過 csv 模組將已經存成檔案的資料讀入
with open('kickstarter_test_2.csv', 'r', newline='', encoding='utf-8') as input_file:
    rows = csv.reader(input_file)
    # 以迴圈輸出每一列，每一列是一個 list
    for row in rows:
        print(row)