#-*- coding: utf-8 -*-
#查詢即時股價
#若是查詢日休市,則取不到資料


import csv
import logging
import random
import urllib3
from datetime import datetime
import ujson as json
from ujson import loads

TSE_URL = 'http://mis.twse.com.tw/'
TSE_CONNECTIONS = urllib3.connection_from_url(TSE_URL)
TWSE_PATH = '/stock/api/getStockInfo.jsp?ex_ch={ex_ch}&json=1&delay={delay}'
logger = logging.getLogger(__name__)

class QuoteStock(object): #Quote-報價
    """docstring for Stock"""
    def __init__(self, no, date, delay=0):
        self.no = no
        self.date = date
        self.delay = delay
        self.__setExchageNo()
        if not date:
          self.date = datetime.now()

    def prepareParam(self):
        return {'ex_ch': self.ex_ch, 'delay': self.delay}

    def fetch_data(self):
        param = self.prepareParam()
        self.result = TSE_CONNECTIONS.urlopen('GET', TWSE_PATH.format(**param)).data
        logger.info(self.result)

    @property
    def data(self):
        self.fetch_data()
        return self.__format_data()

    def __format_data(self):
        stockList = []
        result =  json.loads(self.result)
        if result['rtcode'] == '0000':
            for msg in result['msgArray']:
                stock = Stock(self.no)
                stock.no = msg['c']
                stock.name = msg['n'].encode('utf-8')
                stock.fullname = msg['nf'].encode('utf-8')
                stock.oPrice = msg['o']
                stock.lPrice = msg['l']
                stock.hPrice = msg['h']
                stock.fPrice = msg['z']
                stock.num = msg['tv']
                stock.yPrice = msg['y']
                stock.range = msg['n']
                stockList.append(stock)
                
        else :
            stockList = []

        #parse Json to object 
        return stockList

    def __setExchageNo(self):
        exchage = ""
        for no in self.no.split(";")[0:10]:
            exchage +=  "{exchange}_{no}.tw_{date}|".format(exchange='tse', no =no, date=self.date.strftime('%Y%m%d'))
        self.ex_ch = exchage
    
class Stock(object):
    def __init__(self, no):
        self.name = ''
        self.fullname = ''
        self.oPrice = ''
        self.lPrice = ''
        self.hPrice = ''
        self.fPrice = ''
        self.yPrice = ''
        self.num = ''
        self.range = ''
        self.no = no
