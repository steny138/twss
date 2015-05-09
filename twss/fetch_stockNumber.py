#-*- coding: utf-8 -*-
#更新股票代號

import csv
import logging
import random
import urllib3
import logging
import re
import time
import sys
import datetime
import os
import ujson as json
from ujson import loads
from datetime import datetime
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf8')

NOW = datetime(2014, 7, 3)
SAVEPATH = os.path.join(os.path.dirname(__file__), 'twse_list.csv')#'twss/twse_list.csv'
CODEPATH = os.path.join(os.path.dirname(__file__), 'industry_code.csv')#'twss/industry_code.csv' 
TWSEURL = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX2_print.php?genpage=genpage/Report%(year)s%(mon)02d/A112%(year)s%(mon)02d%(day)02d%%s.php&type=html' % {'year': NOW.year, 'mon': NOW.month, 'day': NOW.day} 
TSE_CONNECTIONS = urllib3.connection_from_url(TWSEURL)
logger = logging.getLogger(__name__)

def fetch_twse_list(isWrite = 0):
    f = open(CODEPATH, 'r')
    all_items = []
    logger.info("Update twse_list.csv in {0}".format(datetime.now().strftime('%Y/%m/%d')))

    #抓所有股票
    for no in csv.DictReader(f):
        time.sleep(0.1)
        page = TSE_CONNECTIONS.urlopen('GET',TWSEURL % no['code'])

        #logging url
        logger.debug(TWSEURL % no['code'])

        htmlDoc = etree.HTML(page.data.lower())
        stockList = htmlDoc.xpath(u"//*[@id=\"tbl-containerx\"]/table/tbody/tr")

        for t in stockList:
            #抓class != digit
            sNo = ''
            sName = ''
            sTypeNo = no['code']
            sTypeName = no['name']
            tds = t.xpath("td[not(contains(@class, 'digit'))]")
            if len(tds) == 3:
                sNo = tds[0].text
                sName = tds[1].text
            elif len(tds) > 3: #多一列 "暫停交易"
                sNo = tds[1].text
                sName = tds[2].text
            all_items.append({'sNo':sNo.strip(),'sName':sName.strip(), 'sTypeNo':sTypeNo.strip(), 'sTypeName': sTypeName.strip()})

            #for test
            if isWrite > 0 : 
                if len(all_items) > 0:
                    return "connect ok"
                else :
                    return "connect failed"

    #write
    nf = open(SAVEPATH, "w")
    w = csv.writer(nf)  
    w.writerow(['證期會代碼', '公司簡稱', '分類代碼', '分類名稱'])
    for item in all_items:
        w.writerow([item['sNo'],item['sName'],item['sTypeNo'],item['sTypeName']])

def fetch_industry_code_list():
    pass

if __name__ == '__main__':
    fetch_twse_list()
    
