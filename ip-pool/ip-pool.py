# coding: utf-8

import MySQLdb
from selenium import webdriver
import traceback
import datetime

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
        f = webdriver.Firefox()
        for i in range(1, 6):
            ip_pool_url = 'http://www.xicidaili.com/nn/' + str(i)
            # document = urllib2.urlopen(ip_pool_url).read()
            f.get(ip_pool_url)
            trs = f.find_elements_by_xpath('//table[@id="ip_list"]/tbody/tr[position()>1]')
            num_records = len(trs)
            for row in trs:
                tds = row.find_elements_by_tag_name("td")
                ip = tds[1].text
                port = tds[2].text
                address = tds[3].text
                secret_type = tds[4].text
                proxy_type = tds[5].text
                speed = tds[6].find_element_by_xpath("//div[@title]").get_attribute("title")[:-1]
                connection = tds[7].find_element_by_xpath("//div[@title]").get_attribute("title")[:-1]
                duration = tds[8].text
                valid_time = tds[9].text
                list_u = [ip, port, address, secret_type, proxy_type, speed, connection, duration, valid_time]
                sql = "INSERT INTO ip_pool(ip, port, address, secret_type, proxy_type, speed, connection, duration, valid_time) VALUES ("
                for item in list_u:
                    sql += "'" + item + "'"
                    sql += ','
                sql = sql[:-1] + ')'
                cur.execute(sql)
                conn.commit()
                print "INSERT ROW {0}".format(','.join([item.encode('utf-8') for item in list_u]))
    except AttributeError:
        traceback.print_exc()
        pass


main()