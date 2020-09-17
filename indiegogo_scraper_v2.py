from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

url = 'https://www.indiegogo.com/projects/transmission-ministry-collective#/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}

driver = webdriver.Chrome(r'C:\Users\USER\Desktop\python\Side Project\pysql\python-selenium\chromedriver.exe')
driver.get(url)
page_content = driver.page_source
soup = BeautifulSoup(page_content, 'html.parser')
row_list = []
story = ''

elements = soup.select('.vueApp')


for element in elements:
    project_name = element.find('div', 'basicsSection-title widescreen t-h4--sansSerif')
    description = element.find('div', 'basicsSection-tagline widescreen t-body--sansSerif--lg')
    num_backer = element.find('span', 't-weight--medium')
    background = element.find_all('p') 
    location = element.find('div', 'basicsCampaignOwner-details-city')
    percentage = element.find('span', 'basicsGoalProgress-progressDetails-detailsGoal-goalPercentageOrInitiallyRaised')
    amount = element.find('span', 'basicsGoalProgress-amountSold t-h5--sansSerif t-weight--bold')
    project_type = element.find_all('span', 'tooltipHover-hoverable--mobile')
    img = element.select('img')
    data = {}
    data['project_name'] = project_name.text.strip()
    data['description'] = description.text.strip()
    data['num_backer'] = num_backer.text.strip()
    for detail in background:   # 背景有很多段，需要迴圈全部印出來
        detail = detail.text
        story += detail
    data['background'] = story
    data['num_img'] = len(img)
    data['percentage'] = percentage.text.strip()
    data['amount'] = amount.text.strip()
    data['location'] = location.text.strip()
    data['project_type'] = project_type[2].text.strip()
    row_list.append(data)

time.sleep(10)

print(type(row_list))
headers = ['project_name', 'description', 'num_backer', 'amount', 'percentage', 'location', 'background', 'num_img', 'project_type']
# 使用檔案 with ... open 開啟 write (w) 寫入檔案模式，透過 csv 模組將資料寫入
with open('indiegogo_project.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, headers)
    # 寫入標題
    dict_writer.writeheader()
    # 寫入值
    dict_writer.writerows(row_list)
# 使用 with ... open 開啟讀取 read (r) 檔案模式，透過 csv 模組將已經存成檔案的資料讀入
with open('indiegogo_project.csv', 'r', newline='', encoding='utf-8') as input_file:
    rows = csv.reader(input_file)
    # 以迴圈輸出每一列，每一列是一個 list
    for row in rows:
        print(row)

driver.quit()