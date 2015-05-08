#-*- coding: utf-8 -*-
import unittest
from datetime import datetime
from types import BooleanType
from types import NoneType
import twss 
import logging
import logging.config

class TestTwss(unittest.TestCase):
    '''
    def get_data(self):
        self.stock_no = '2618'
        self.data = grs.Stock(self.stock_no)

    def test_stock(self):
        self.get_data()
        assert self.data.info[0] == self.stock_no

    def test_best_buy_or_sell(self):
        self.get_data()
        assert isinstance(grs.BestFourPoint(self.data).best_four_point(),
                          (tuple, NoneType))

    def test_moving_average(self):
        self.get_data()
        result = self.data.moving_average(3)
        assert isinstance(result[0], list)
        assert isinstance(result[1], int)
        assert result == self.data.MA(3)
    '''

    def __get_data(self):
        self.datas = twss.fetch_from_twse.QuoteStock('2330;3257;0050;0056;2731', datetime.now()).data
        return self.datas

    #@staticmethod
    def test_twse_no(self):
        datas = self.__get_data()
        assert len(datas) == 5
#set logger
def main():
    logging.basicConfig(level=logging.WARNING)
    logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
    #logger = logging.getLogger( __name__ )

if __name__ == '__main__':
    main()
    unittest.main()

