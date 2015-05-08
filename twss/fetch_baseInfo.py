#-*- coding: utf-8 -*-

import csv
import logging
import random
import urllib3
from datetime import datetime
import ujson as json
from ujson import loads
import logging
import re
from lxml import etree


import sys
reload(sys)
sys.setdefaultencoding('utf8')

NOW = datetime(2014, 7, 3)
SAVEPATH = '../twss/twse_list.csv'
CODEPATH= 'industry_code.csv'

TWSEURL = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX2_print.php?genpage=genpage/Report%(year)s%(mon)02d/A112%(year)s%(mon)02d%(day)02d%%s.php&type=html' % {'year': NOW.year, 'mon': NOW.month, 'day': NOW.day} 
TSE_CONNECTIONS = urllib3.connection_from_url(TWSEURL)

def fetch_twse_list():
   
    f = open(CODEPATH, 'r')
    all_items = []
    re_pattern = re.compile(r'".*"')
    p_pattern = re.compile(ur'.*:.*\n')
    #replace_pattern = regex.sub("interfaceOpDataFile %s" % fileIn, line)
    #抓所有股票
    for no in csv.DictReader(f):
        page = TSE_CONNECTIONS.urlopen('GET',TWSEURL % no['code'])
        htmlDoc = etree.HTML(page.data.lower())
        stockList = htmlDoc.xpath(u"//*[@id=\"tbl-containerx\"]/table/tbody/tr")

        for t in stockList:
            print t.text
            #抓class != digit
            #tds = t.xpath("td[not(contains(@class, 'digit'))]")
            #print(tds[1].text)
            #print(tds[2].text)
            #print(tds[5].text)
            #print(tds[6].text)


    '''
    for no in csv.DictReader(f):
        print TWSEURL % no['code']
        response = TSE_CONNECTIONS.urlopen('GET',TWSEURL % no['code'])
        responseStr = re_pattern.sub('',response.data.decode('CP950'))

        responseStr = p_pattern.sub('', responseStr)

        responseStr = responseStr.strip().decode("utf-8")
        f2 = open('twse_list_test.csv', 'w+') 
        f2.write(responseStr)
        break;

    f3 = open('../twss/twse_list_test.csv', 'r')
    for t in csv.DictReader(f3): 
        print t
    '''
    '''
    print responseStr
    for key in csv.DictReader(responseStr): 
        print key.keys()
    break;

    '''
    #寫入csv
    '''
    with open(SAVEPATH, 'w') as files:
        csv_file = csv.writer(files)
        #csv_file.writerow(['文件更新', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'x', 'x'])
        csv_file.writerow(['UPDATE', datetime.now().strftime('%Y/%m/%d'), 'x', 'x'])
        csv_file.writerow(['證期會代碼', '公司簡稱', '分類代碼', '分類名稱'])
        for i in sorted(all_items):
            csv_file.writerow(all_items[i])
    '''



if __name__ == '__main__':
    fetch_twse_list()
    
