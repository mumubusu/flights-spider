import urllib2
import psycopg2
import data
import time
import json


def address_lnglat(address):
    url = "http://api.map.baidu.com/geocoder/v2/?address=" + address + "&output=json&ak=d4aC3XR1Xmpbrcz36VGMaIcj"
    html = urllib2.urlopen(url)
    document = html.read()
    print document
    json_data = json.loads(document)
    try:
        lng = str(json_data["result"]["location"]["lng"])
        lat = str(json_data["result"]["location"]["lat"])
    except:
        [lng, lat] = ['', '']
    return [lng, lat]

def main1():
    conn = psycopg2.connect(database="postgres", user="postgres", password="", host="localhost", port="5432")
    cursor = conn.cursor()
    for airport in data.airports:
        address = airport[0]
        [lng, lat] = address_lnglat(address)
        sql = "insert into public.airports(address,lng,lat) values ('"+address+"','"+lng+"','"+lat+"')"
        cursor.execute(sql)
        conn.commit()
        print address
        time.sleep(0.3)

def main2():
    conn = psycopg2.connect(database="postgres", user="postgres", password="", host="localhost", port="5432")
    cursor = conn.cursor()
    sql = 'select * from public.airports'
    cursor.execute(sql)
    airports_db = cursor.fetchall()
    for item in airports_db:
        for airport in data.airports:
            if airport[0] == item[1]:
                sql = "update public.airports set three_code = '"+airport[1]+"' where id="+str(item[0])
                cursor.execute(sql)
                conn.commit()
                break
    conn.close()

main2()