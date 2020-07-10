import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
import pymysql
import json

URL = "http://www.allconferences.com/search/index/viewCategorySearch:/Category__parent_id:1/showLastConference:0/page:{}/"

db = pymysql.connect(host='localhost', user='root',
                     password='123456', port=3306, db='mydb')
cursor = db.cursor()
sql = "INSERT INTO data_forum('title','location','venue', 'begin','end','synopsis','link') values(%s,%s,%s,%s,%s,%s,%s)"


def parse(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    data = []
   # for each in soup.find_all(class_= "conferenceDescription" ):
    for each in soup.find_all(class_="listing_content"):
        try:
            title = each.find(class_="conferenceHead").find(
                'h2').text.replace('\n', '')
        except:
            title = 'None'
        try:
            tmp = each.find(class_="venue_info").find_all('a')
            location = tmp[1].text.replace(
                '\n', '')+','+tmp[2].text.replace('\n', '')
        except:
            location = 'None'
        try:
            venue = each.find(class_="venue_info").find(
                'a').text.replace('\n', '')
        except:
            venue = 'None'
        try:
            synopsis = each.find(class_="conferenceDescription").a.text.replace(
                '\n', '')
        except:
            synopsis = 'None'
        try:
            begin_txt = each.find(class_="conferenceDate floatRight").find(
                'span', {'class': "begin_txt"}).a.text.replace('\n', '')
        except:
            begin_txt = 'None'
        try:
            end_txt = each.find(class_="conferenceDate floatRight").find_all(
                'span')[1].text.replace('Ends\r', '').replace('\n', '')
        except:
            end_txt = 'None'
        try:
            link = each.a.get('href')
        except:
            link = 'None'

        item = {
            'title': title,
            'location': location,
            'venue': venue,
            'begin': begin_txt,
            'end': end_txt,
            'synopsis': synopsis,
            'link': link
        }
        data.append(item)

    return data


def save_to_MYSQL(new_data):
    try:
        cursor.execute(sql, (new_data['title'], new_data['location'], new_data['venue'],
                             new_data['begin'], new_data['end'], new_data['synopsis'], new_data['link']))
        db.commit()
        print('插入数据成功')
    except Exception as e:
        print('插入数据失败！！', e)
        db.rollback()


if __name__ == '__main__':
    data = []
    for i in range(0, 21):
        url = URL.format(i)
        newdata = parse(url)
        data.append(newdata)
        for item in newdata:
            save_to_MYSQL(item)

    with open('forum.json', 'a+', encoding='utf-8') as f:
        for item in data:
            json.dump(item, f, ensure_ascii=False)
