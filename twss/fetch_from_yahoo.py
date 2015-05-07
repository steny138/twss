import csv
#import logging
import random
import urllib3
import ssl
from lxml import etree;
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()
urllib3.disable_warnings()

'''
import certifi

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED', # Force certificate check.
    ca_certs=certifi.where(),  # Path to the Certifi bundle.
)

try:
    r = http.request('GET', 'https://tw.stock.yahoo.com/q/q?s=2330')
except urllib3.exceptions.SSLError as e:
	print('fuck')
    # Handle incorrect certificate error.

print(r.data)
'''
#urllib3.disable_warnings()
no='2330'

#TSE_URL = 'http://mis.twse.com.tw/'

TSE_URL = 'https://tw.stock.yahoo.com/'
TSE_CONNECTIONS = urllib3.connection_from_url(TSE_URL)

#page = TSE_CONNECTIONS.urlopen('GET','/data/%s.csv?r=%s' % (no,
                        #random.randrange(1, 10000))).data

page = TSE_CONNECTIONS.urlopen('GET', '/q/q?s=3257').data

htmlDoc = etree.HTML(page.lower())

hrefs = htmlDoc.xpath(u"//center/table[2]/tbody/tr/td/table/tbody/tr[2]/td[3]")

##yui_3_5_1_13_1430973174348_6 > table:nth-child(16) > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(3) > b
print hrefs
for href in hrefs:
	print href.attrib

