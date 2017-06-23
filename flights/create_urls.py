import data
import psycopg2

conn = psycopg2.connect(database="postgres",user="postgres",password="",host="localhost",port="5432")
cursor = conn.cursor()
date = '20170501'
for airport in data.airports:
    for airport2 in data.airports:
        if airport[1] != airport2[1]:
            url = "http://www.variflight.com/flight/" + airport[1] + "-" + airport2[
                1] + ".html?AE71649A58c77&fdate=" + date
            sql = "insert into public.urls(url,ori,des,ori_name,des_name,flag) values ('"+url+"','"+airport[1]+"','"+airport2[1]+"','"+airport[0]+"','"+airport2[0]+"','0')"
            cursor.execute(sql)
            conn.commit()