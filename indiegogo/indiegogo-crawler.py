from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import random
import pandas as pd 

data_path = 'C:/Users/USER/Desktop/論文/'
indiegogo = pd.read_csv(data_path + 'indiegogo_url_green_tech.csv', engine = 'python')



for project_url in indiegogo['project_url']:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
    driver = webdriver.Chrome(r'.\chromedriver.exe')
    driver.get('https://www.indiegogo.com/' + project_url)
    time.sleep(random.randint(10, 60))
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
        data = {}
        data['project_name'] = project_name.text.strip()
        data['description'] = description.text.strip()
        data['num_backer'] = num_backer.text.strip()
        for detail in background:   # 背景有很多段，需要迴圈全部印出來
            detail = detail.text
            story += detail
        data['background'] = story
        data['percentage'] = percentage.text.strip()
        data['amount'] = amount.text.strip()
        data['location'] = location.text.strip()
        data['project_type'] = project_type[2].text.strip()
        row_list.append(data)
        driver.quit()
        headers = ['project_name', 'description', 'num_backer', 'amount', 'percentage', 'location', 'background', 'num_img', 'project_type']

# 等所有 for 迴圈資料都放入 row_list 後再寫入檔案，這樣寫入檔案就是最後 for 迴圈都跑完的資料一起寫入
with open('indiegogo_project.csv', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, headers)
    # 寫入標題
    dict_writer.writeheader()
    # 寫入值
    dict_writer.writerows(row_list)