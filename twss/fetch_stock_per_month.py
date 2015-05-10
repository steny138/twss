#-*- coding: utf-8 -*-
#擷取每月股價

import csv
import logging
import random
import urllib3
import os
import sys
from datetime import datetime
from cStringIO import StringIO
from dateutil.relativedelta import relativedelta


TWSE_URL = "http://www.twse.com.tw/"
TWSE_CONNECTION = urllib3.connection_from_url(TWSE_URL)
TWSE_PATH = "/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report{year:4d}{month:02d}/{year:4d}{month:02d}_F3_1_8_{no}.php&type=csv&r={random}"

logger = logging.getLogger(__name__)

class QuoteStockPerMonth(object):
	"""擷取每月股價"""
	"""param int year"""
	"""param int month"""
	"""param int monthAgo default = 0"""
	"""data回傳List 內容是該月的股價by day"""
	def __init__(self, no, year, month, monthAgo=0):
		self.no = no
		self.year  = year
		self.month = month
		self.ago = monthAgo
		self.stockList = []
		b = self.fetch_data()
		if b:
			logger.info('{0} {1}/{2:02d} 共{3}個月 有{4}天開市'.format(self.no, self.year, self.month, self.ago +1, len(self.data)))

	def fetch_data(self):
		if self.no:
			try:
				for i in xrange(0, self.ago + 1):
					date = datetime(self.year, self.month, 1) - relativedelta(months=i)
					page = self.__fetch_data(date.year, date.month)
					csv_files = csv.reader(StringIO(page))
						#if csv_files:
					for row in csv_files:
						if len(row) > 1:
							self.stockList.append(self.__translate(row))
				return True
			except Exception, e:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				logger.warning("擷取歷史股價失敗 {0} -- in : {1}, {2}".format(str(e), fname, exc_tb.tb_lineno))
			
		self.stockList = []
		return False

	def __fetch_data(self, year, month):
		param = self.__getParam(year, month)
		page = TWSE_CONNECTION.urlopen('GET', TWSE_PATH.format(**param))
		logger.debug(page.data)
		return page.data
		
		
		
	def __translate(self, row):
		#開始解析
		"""
		0: 日期
		1: 成交股數
		2: 成交金額
		3: 開盤價
		4: 最高價
		5: 最低價
		6: 收盤價
		7: 漲跌價差
		8: 成交筆數
		"""
		stock = StockPerDay(self.no)
		stock.date = row[0]
		stock.volume = row[1]
		stock.amount = row[2]
		stock.open = row[3]
		stock.high = row[4]
		stock.low = row[5]
		stock.close = row[6]
		stock.range = row[7]
		stock.count = row[8]
		return stock
		pass

	def __getParam(self, year, month):
		return {'year': year, 'month': month, 'no' : self.no, 'random': random.randrange(1, 1000000)}

	@property
	def data(self):
		return self.stockList
	

class StockPerDay(object):
	"""每日股價用"""
	def __init__(self,no):
		super(StockPerDay, self).__init__()
		self.no = no
		self.date = ''
		self.volume = 0
		self.count = 0
		self.amount =0
		self.open = 0
		self.close = 0
		self.high = 0
		self.low = 0
		self.range = ''

"""	
#quote.fetch_data()

print len(QuoteStockPerMonth('2330', 2015, 3, 1).data)

	
for x in QuoteStockPerMonth('2330').data:
	print x.no, x.date,x.volume, x.close
"""