import requests
import MySQLdb
import time

def test_get():
    while True:
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='',
            db='flight-spider',
        )
        print "Connected!"
        try:
            sql = "SELECT ip, port from ip_pool order by rand() limit 1"
            cur = conn.cursor()
            cur.execute(sql)
            results = cur.fetchall()
            proxies = {
                'http': 'http://{0}:{1}'.format(results[0][0], results[0][1]),
                'https': 'http://{0}:{1}'.format(results[0][0], results[0][1])
            }
            resp = requests.get('http://www.variflight.com/flight/PEK-PVG.html?AE71649A58c77', proxies=proxies, allow_redirects=False, timeout=10)
            if resp.status_code != 200:
                raise Exception("Wrong status code.")
            else:
                print resp.content
        except Exception,e:
            print str(e)
            time.sleep(2)
            print 'sleep'
            test_get()

test_get()