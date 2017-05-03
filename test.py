# coding:utf-8
import threading
from time import sleep

def test1(s=0,num=100):
    for i in range(s,num):
        print i
        print '\r\n'
        sleep(0.1)



threads = []
t1 = threading.Thread(target=test1,args=(0,100,))
threads.append(t1)
t2 = threading.Thread(target=test1,args=(100,200,))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print 'finish!'