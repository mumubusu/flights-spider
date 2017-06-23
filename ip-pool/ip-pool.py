# coding: utf-8

import MySQLdb
import urllib2
from selenium import webdriver
import traceback

def main():
    try:
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='',
            db='flight-spider',
        )
        print "Connected!"
        cur = conn.cursor()
        f = webdriver.Firefox('/Users/quyihang/Downloads/')
        for i in range(1, 6):
            ip_pool_url = 'http://www.xicidaili.com/nn/' + str(i)
            # document = urllib2.urlopen(ip_pool_url).read()
            f.get(ip_pool_url)
            trs = f.find_elements_by_xpath('//table[@id="ip_list"/tbody/tr[position()>1]')
            num_records = len(trs)
            for row in trs:
                tds = row.find_elements_by_tag_name("td")
                print tds
    except AttributeError:
        traceback.print_exc()
        pass


main()