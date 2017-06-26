# coding: utf-8

import MySQLdb
from selenium import webdriver
import traceback
import datetime
import time

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
        ip_pool_url = 'http://www.xicidaili.com/nn/1'
        while True:
            now = datetime.datetime.now()
            target_time = datetime.datetime(2017,6,26,11,10,0)
            if now >= target_time:
                print "现在是：%s，目标时间：%s，开始爬取ip池" % (now, target_time)
                f.get(ip_pool_url)
                trs = f.find_elements_by_xpath('//table[@id="ip_list"]/tbody/tr[position()>1]')
                for row in trs:
                    tds = row.find_elements_by_tag_name("td")
                    ip = tds[1].text
                    sql = "SELECT count(*) FROM ip_pool where ip = '%s';" % (ip)
                    cur.execute(sql)
                    results = cur.fetchall()
                    if results[0][0] > 0:
                        print "已经存在, 跳过, %s" % (ip.encode('utf-8'))
                        continue
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
                    sql = sql[:-1] + ');'
                    cur.execute(sql)
                    conn.commit()
                    print "INSERT ROW {0}".format(','.join([item.encode('utf-8') for item in list_u]))
                target_time += datetime.timedelta(minutes=5)
                print "在等待, {0}".format(str(now))
            else:
                print "在等待, {0}".format(str(now))
            time.sleep(60)
    except AttributeError:
        traceback.print_exc()
        main()


main()