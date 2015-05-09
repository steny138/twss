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
                    result._no = no

                    result._type = firstTr[1].text.encode('utf-8').strip()
                    
                    result._cFullname = infoTrs[1].xpath(u"td")[0].text.encode('utf-8').strip()
                    result._callPhone = infoTrs[1].xpath(u"td")[1].text.encode('utf-8').strip()

                    result._address = infoTrs[2].xpath(u"td")[0].text.encode('utf-8').strip()

                    result._chairman = infoTrs[3].xpath(u"td")[0].text.encode('utf-8').strip()
                    result._manager = infoTrs[3].xpath(u"td")[1].text.encode('utf-8').strip()


                    result._idno = infoTrs[7+AddRowNum].xpath(u"td")[1].text.encode('utf-8').strip()

                    result._capital = infoTrs[8+AddRowNum].xpath(u"td")[0].text.encode('utf-8').strip()
                    #result._startDate = infoTrs[8].xpath(u"td")[1].text.encode('utf-8').strip()

                    
                    result._ename = infoTrs[19+AddRowNum].xpath(u"td")[0].text.encode('utf-8').strip()
                    
                    result._eFullname = infoTrs[20+AddRowNum].xpath(u"td")[0].text.encode('utf-8').strip()
                    

                    result._fax = infoTrs[22+AddRowNum].xpath(u"td")[0].text.encode('utf-8').strip()
                    result._email = infoTrs[22+AddRowNum].xpath(u"td")[1].text.encode('utf-8').strip()

                    result._webUrl = infoTrs[23+AddRowNum].xpath(u"td")[0].text.encode('utf-8').strip()

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
        self._type = ''
        self._name = ''
        self._address = ''
        self._callPhone = ''
        self._chairman = ''
        self._manager = ''
        self._startDate = ''
        self._idno = ''
        self._capital = ''
        self._cFullname = ''
        self._ename = ''
        self._eFullname = ''
        self._fax = ''
        self._webUrl = ''
        self._no = ''
    @property
    def no(self):       #代號
        return  self._no

    @property
    def type(self):       #行業別
        return  self._type

    @property
    def cname(self):    #中文簡稱
        return self._name

    @property
    def address(self):  #中文地址
        return self._address

    @property
    def callPhone(self):    #公司電話
        return self._callPhone

    @property
    def chairman(self):     #董事長
        return self._chairman
    
    @property
    def manager(self):      #總經理
        return self._manager
    @property
    def startDate(self):    #上市日期
        return self._startDate

    @property
    def idno(self):         #統一編號
        return self._idno
    @property
    def capital(self):      #資本額
        return self._capital
    @property
    def cFullname(self):    #中文全稱
        return self._cFullname
    @property
    def ename(self):        #英文簡稱
        return self._ename
    @property
    def eFullname(self):    #英文全稱
        return self._eFullname
    @property
    def fax(self):          #傳真
        return self._fax
    @property
    def webUrl(self):       #網址
        return self._webUrl

