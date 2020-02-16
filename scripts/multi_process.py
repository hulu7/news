# -*- coding: utf-8 -*-
from multiprocessing import Process
import time
x=1000
def task(n):
    print('%s is runing' %n)
    time.sleep(n)

if __name__ == '__main__':
    start_time=time.time()
    while True:
        p_l=[]
        for i in range(1,4):
            p=Process(target=task,args=(i,))
            p_l.append(p)
            p.start()

        for p in p_l:                       #1 is runing
            p.join()                        #3 is runing
        print('master',(time.time() - start_time)) #2 is runing    主  3.112313