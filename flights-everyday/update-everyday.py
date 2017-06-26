# coding:utf-8

import urllib2
import bs4
import time
import datetime
import MySQLdb
import urllib
import random
import traceback
import requests
import threading


proxyip = '0.0.0.0:000'

class parseDocument:
    def __init__(self, document):
        self.document = document

    def parse(self):
        res_list = []
        try:
            self.soup = bs4.BeautifulSoup(self.document, 'html.parser')
            lis = self.soup.find_all('li', attrs={"style": "position: relative;"})
            for li in lis:
                index = 7
                if li.contents[5].encode('utf-8') != '  共享航班	':
                    index = 9
                soup2 = bs4.BeautifulSoup(str(li.contents[index].contents[1]), 'html.parser')
                company = soup2.find_all('a')[0].contents[0].encode('utf-8')
                flight_num = soup2.find_all('a')[1].contents[0].encode('utf-8')
                start_time = li.contents[index].contents[3].contents[0].replace('\n','').replace('\t','').encode('utf-8')
                end_time = li.contents[index].contents[9].contents[0].replace('\n','').replace('\t','').encode('utf-8')
                origin = li.contents[index].contents[7].contents[0].encode('utf-8')
                destination = li.contents[index].contents[13].contents[0].encode('utf-8')
                res_list.append([company, flight_num, start_time, end_time, origin, destination])
        except:
            traceback.print_exc()
        return res_list

def abuyun(targetUrl):
    proxyHost = "proxy.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "HV1LZ39I846185AD"
    proxyPass = "3FCA3479141C30C0"
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    resp = requests.get(targetUrl, proxies=proxies)
    return [resp.status_code, resp.text]

def wuyou():
    order = "11c85067059d71c1b412fa34e2cc36d3"
    apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order
    res = urllib2.urlopen(apiUrl).read().strip("\n")
    ips = res.split("\n")
    proxyip = random.choice(ips)
    return proxyip


def delete_ori_des(list, ori, des):
    print len(list)
    for item in list:
        if item[10] == 1:
            list.remove(item)
    for item in list:
        if item[3] == ori and item[4] == des:
            list.remove(item)
    print len(list)
    return list


def main(thread):
    try:
        conn = MySQLdb.connect(
            host='localhost',
            port = 3306,
            user='',
            passwd='',
            db ='test',
            )
        print "Connected!"
        cur = conn.cursor()
        num = cur.execute("SELECT * FROM url_crab WHERE (flag <> 1 OR flag IS NULL) AND thread = %d" % thread)
        info = list(cur.fetchmany(num))
        count = 0
        while len(info) > 0:
            inf = info[0]
            ori = inf[1]; des = inf[2]
            url = "http://www.variflight.com/flight/"+ori+"-"+des+".html?AE71649A58c77"
            print url
            count += 1
            print "thread: %d" % thread
            time.sleep(0.2)
            # proxyip = wuyou()
            # document = urllib.urlopen(url, proxies={'http':'http://' + proxyip}).read()
            # document = urllib2.urlopen(url).read()
            document = abuyun(url)[1]
            pd = parseDocument(document)
            pd_list = pd.parse()
            print 'pd count: '+str(len(pd_list))
            for record in pd_list:
                [company, flight_num, stime, etime, origin, destination] = record
                try:
                    num = cur.execute("update petal_airlines set plan_start = '"+stime+"', plan_reach='"+etime+"' where (flight_num='"+flight_num+"' and ori_code='"+ori+"' and des_code='"+des+"')")
                    conn.commit()
                    if num == 0:
                        sql = "INSERT INTO petal_airlines(company, flight_num, ori_code, des_code, plan_start, plan_reach) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(company, flight_num, origin, destination, stime, etime)
                        cur.execute(sql)
                        conn.commit()
                except:
                    pass
            num = cur.execute(
                "update url_crab set flag = 1 where (ori='" + ori + "' and des='" + des + "')")
            conn.commit()
            num = cur.execute("SELECT * FROM url_crab WHERE (flag <> 1 OR flag IS NULL) AND thread = %d" % thread)
            info = list(cur.fetchmany(num))
            print "info length: %d" % num
        cur.close()
        conn.close()
    except:
        traceback.print_exc()
        time.sleep(1)
        main(thread)

def a_fresh_new_day():
    try:
        conn = MySQLdb.connect(
            host='localhost',
            port = 3306,
            user='',
            passwd='',
            db ='test',
            )
        print "Connected!"
        cur = conn.cursor()
        sql = "UPDATE petal_airlines SET plan_start = null, plan_reach = null"
        cur.execute(sql)
        cur.commit()
        sql = "UPDATE url_crab SET flag = 0"
        cur.execute(sql)
        cur.commit()
        cur.close()
        conn.close()
    except:
        traceback.print_exc()


if __name__ == '__main__':
    target_time = datetime.datetime(2017, 6, 26, 4, 0, 0)
    while True:
        now = datetime.datetime.now()
        if now >= target_time:
            #  a_fresh_new_day()
            threads = []
            for i in range(4):
                t = threading.Thread(target=main, args=(i,))
                threads.append(t)
            for t in threads:
                t.setDaemon(True)
                t.start()
            t.join()
            target_time += datetime.timedelta(days = 1)
        time.sleep(600)