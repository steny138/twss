#-*- coding: utf-8 -*-

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

class QuoteStock(object):
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
                stock._no = msg['c']
                stock._name = msg['n'].encode('utf-8')
                stock._fullname = msg['nf'].encode('utf-8')
                stock._oPrice = msg['o']
                stock._lPrice = msg['l']
                stock._hPrice = msg['h']
                stock._fPrice = msg['z']
                stock._num = msg['tv']
                stock._yPrice = msg['y']
                stock._range = msg['n']
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
        self._name = ''
        self._fullname = ''
        self._oPrice = ''
        self._lPrice = ''
        self._hPrice = ''
        self._fPrice = ''
        self._yPrice = ''
        self._num = ''
        self._range = ''
        self._no = no
    @property
    def no(self):
        return  self._no

    @property
    def name(self):
        return self._name
    @property
    def fullname(self):
        return self._fullname
    @property
    def oPrice(self):
        return self._oPrice
    @property
    def lPrice(self):
        return self._lPrice
    @property
    def hPrice(self):
        return self._hPrice
    @property
    def fPrice(self):
        return self._fPrice
    @property
    def num(self):
        return self._num
    @property
    def yPrice(self):
        return self._yPrice
    @property
    def range(self):
        return self._range

