# coding:utf-8

import data
import urllib2
import bs4
import psycopg2
import time
import threading

SLEEP_TIME = 0.1
time0 = time.time()
def abuyun(targetUrl):
    # 代理服务器
    proxyHost = "proxy.abuyun.com"
    proxyPort = "9010"

    # 代理隧道验证信息
    proxyUser = "H172E9M81S36NS5P"
    proxyPass = "A933F5C70D3069EB"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }

    proxy_handler = urllib2.ProxyHandler({
        "http"  : proxyMeta,
        "https" : proxyMeta,
    })

    opener = urllib2.build_opener(proxy_handler)

    #opener.addheaders = [("Proxy-Switch-Ip", "yes")]
    urllib2.install_opener(opener)
    resp = urllib2.urlopen(targetUrl).read()
    return resp


class parseDocument:
    def __init__(self, document):
        self.document = document

    def parse(self):
        self.soup = bs4.BeautifulSoup(self.document, 'html.parser')
        lis = self.soup.find_all('li', attrs={"style": "position: relative;"})
        res_list = []
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
        return res_list


def thread_spider(urls, cursor, conn, thread_num):
    date = '20170501'
    for item in urls:
        id = item[0]; url = item[1]; ori=item[2]; des = item[3]; ori_name = item[4]; des_name = item[5]; flag = item[6]
        if flag == '1':
            continue
        document = abuyun(url)
        # document = urllib2.urlopen(url).read()
        pd = parseDocument(document)
        res_list = pd.parse()
        time.sleep(SLEEP_TIME)
        if len(res_list) == 0:
            sql = "update public.urls set flag = 1 where id = "+str(id)
            cursor.execute(sql)
            conn.commit()
            time1 = time.time() - time0
            print 'no '+str(id) + ' ' + str(time1) + ' ' + str(thread_num)
            continue
        for res in res_list:
            res.append(ori_name)
            res.append(des_name)
            res.append(date)
            sql = "insert into public.flights2(company,flight_num,start_time,end_time,origin,destination,ori,des,date) values ("
            for item in res:
                sql += "'" + item + "'"
                sql += ','
            sql = sql[:-1] + ')'
            cursor.execute(sql)
            conn.commit()
            print sql
            print url
            print str(id)
            time1 = time.time() - time0
            print str(time1)
        sql = "update public.urls set flag = 1 where id = "+str(id)
        cursor.execute(sql)
        conn.commit()

def main():
    try:
        conn = psycopg2.connect(database="postgres",user="postgres",password="",host="localhost",port="5432")
        cursor = conn.cursor()
        count = 0
        sql = 'select * from public.urls'
        cursor.execute(sql)
        urls = cursor.fetchall()
        urls1 = urls[20322:21500]
        urls2 = urls[21500:22000]
        urls3 = urls[22000:34000]
        urls4 = urls[34000:]
        threads = []
        t1 = threading.Thread(target=thread_spider, args=(urls1, cursor, conn, 1,))
        threads.append(t1)
        t2 = threading.Thread(target=thread_spider, args=(urls2, cursor, conn, 2,))
        threads.append(t2)
        t3 = threading.Thread(target=thread_spider, args=(urls3, cursor, conn, 3,))
        threads.append(t3)
        t4 = threading.Thread(target=thread_spider, args=(urls4, cursor, conn, 4,))
        threads.append(t4)
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
    except:
        time.sleep(3)
        main()

if __name__ == '__main__':
    main()