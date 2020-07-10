import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
import pymysql
import json

URL = "https://www.indeed.com/jobs?q=Research+Assistant&start={}0"

db = pymysql.connect(host='localhost', user='root',
                     password='123456', port=3306, db='mydb')
cursor = db.cursor()
sql = "INSERT INTO data_ra('title','location','company', 'frequency','synopsis','link') values(%s,%s,%s,%s,%s,%s)"


def parse(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    for each in soup.find_all(class_="result"):
        try:
            title = each.find(class_='jobtitle').text.replace('\n', '')
        except:
            title = 'None'
        try:
            location = each.find(
                'span', {'class': "location"}).text.replace('\n', '')
        except:
            location = 'None'
        try:
            company = each.find(class_='company').text.replace('\n', '')
        except:
            company = 'None'
        try:
            synopsis = each.find(class_='summary').find(
                'li').text.replace('\n', '')
        except:
            synopsis = 'None'
        try:
            tmp = each.a
            link = 'https://www.indeed.com'+tmp.get('href')
        except:
            link = 'None'
        item = {
            'title': title,
            'location': location,
            'company': company,
            'frequency': frequency,
            'synopsis': synopsis,
            'link': link
        }
        data.append(item)
    return data


def save_to_MYSQL(new_data):
    try:
        cursor.execute(sql, (new_data['title'], new_data['location'], new_data['company'],
                             new_data['frequency'], new_data['synopsis'], new_data['link']))
        db.commit()
        print('插入数据成功')
    except Exception as e:
        print('插入数据失败！！', e)
        db.rollback()


if __name__ == '__main__':
    data = []
    for i in range(0, 40):
        url = URL.format(i)
        newdata = parse(url)
        data.append(newdata)
        for item in newdata:
            save_to_MYSQL(item)
    with open('ra.json', 'a+', encoding='utf-8') as f:
        for item in data:
            json.dump(item, f, ensure_ascii=False)
