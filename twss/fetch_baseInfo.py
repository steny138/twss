#-*- coding: utf-8 -*-
#股票基本資料

import logging
import urllib
import urllib3
from datetime import datetime
import ujson as json
from ujson import loads
from lxml import etree

import os
import sys
logger = logging.getLogger(__name__)


INFO_URL = "http://mops.twse.com.tw/"
INFO_PATH = "/mops/web/ajax_t05st03"
INFO_CONNECTIONS = urllib3.connection_from_url(INFO_URL)


class StockInfo(object):
    """查詢股票基本資料用"""
    def __init__(self, no):
        super(StockInfo, self).__init__()
        self.no = no
        self.__fetch_stockInfo()

    def __fetch_stockInfo(self):
        field = {'firstin': '1', 'co_id': self.no}
        d = urllib.urlencode(field)
        page = INFO_CONNECTIONS.urlopen('POST', INFO_PATH, d)
        self.result = page.data

    def __translateModel(self):
        hparser = etree.HTMLParser(encoding='utf-8')
        html = etree.HTML(self.result, hparser)

        logger.debug(etree.tostring(html))

        #開始讀取
        #先抓 stock_no
        infoTrs = html.xpath(u"//body/table[2]/tr")
        if infoTrs:
            firstTr = infoTrs[0].xpath(u"td")
            if firstTr:
                try:
                    #29
                    #26
                    AddRowNum = 0
                    if len(infoTrs) > 26:
                        AddRowNum = 3

                    no =firstTr[0].text
                    result = Info()
                    result.no = no

                    result.type = firstTr[1].text.encode('utf-8').strip()
                    
                    result.cFullname = infoTrs[1].xpath(u"td")[0].text.encode('utf-8').strip()
                    result.callPhone = infoTrs[1].xpath(u"td")[1].text.encode('utf-8').strip()

                    result.address = infoTrs[2].xpath(u"td")[0].text.encode('utf-8').strip()

                    result.chairman = infoTrs[3].xpath(u"td")[0].text.encode('utf-8').strip()
                    result.manager = infoTrs[3].xpath(u"td")[1].text.encode('utf-8').strip()


                    result.idno = infoTrs[7+AddRowNum].xpath(u"td")[1].text.encode('utf-8').strip()

                    result.capital = infoTrs[8+AddRowNum].xpath(u"td")[0].text.encode('utf-8').strip()
                    #result._startDate = infoTrs[8].xpath(u"td")[1].text.encode('utf-8').strip()

                    
                    result.ename = infoTrs[19+AddRowNum].xpath(u"td")[0].text.encode('utf-8').strip()
                    
                    result.eFullname = infoTrs[20+AddRowNum].xpath(u"td")[0].text.encode('utf-8').strip()
                    

                    result.fax = infoTrs[22+AddRowNum].xpath(u"td")[0].text.encode('utf-8').strip()
                    result.email = infoTrs[22+AddRowNum].xpath(u"td")[1].text.encode('utf-8').strip()

                    result.webUrl = infoTrs[23+AddRowNum].xpath(u"td")[0].text.encode('utf-8').strip()

                    logger.info('{0}/{1}'.format(result.cFullname, result.capital))

                    return result
                except Exception, e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    #raise e
                    logger.warning('轉換股票基本資料發生錯誤 {0} -- in : {1}, {2}'.format(str(e),fname, exc_tb.tb_lineno))
        return None           
        #return new Info();
    @property
    def data(self):
        return self.__translateModel()
        #return __translateModel()
    

class Info(object):
    def __init__(self):
        self.type = ''     #行業別
        self.name = ''     #中文簡稱
        self.address = ''  #中文地址
        self.callPhone = ''#公司電話
        self.chairman = '' #董事長
        self.manager = ''  #總經理
        self.startDate = ''#上市日期
        self.idno = ''     #統一編號
        self.capital = ''  #資本額
        self.cFullname = ''#中文全稱
        self.ename = ''    #英文簡稱
        self.eFullname = ''#英文全稱
        self.fax = ''      #傳真
        self.webUrl = ''   #網址
        self.no = ''       #代號
    