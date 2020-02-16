# -*- coding: utf-8 -*-
from multiprocessing import Process
from multiprocessing import Pool
import time
import os
# x=1000
# def task(n):
#     print('%s is runing' %n)
#     time.sleep(n)
#
# if __name__ == '__main__':
#     start_time=time.time()
#     while True:
#         p_l=[]
#         for i in range(1,4):
#             p=Process(target=task,args=(i,))
#             p_l.append(p)
#             p.start()
#
#         for p in p_l:                       #1 is runing
#             p.join()                        #3 is runing
#         print('master',(time.time() - start_time)) #2 is runing    主  3.112313

def run2(n, i):
    print '{0} - {1} is running'.format(n, i)

def run(n):
    time.sleep(1)
    p = Pool(2)
    for i in range(4):
        p.apply_async(run2, args=(str(n), str(i)))
    p.close()
    p.join()
    return n

def get_pool(n=2):
    p = Pool(n)
    for i in range(4):
        p.apply_async(run, args=(str(i),))
    p.close()
    p.join()

if __name__ == '__main__':
    get_pool()
    print('ths process is ended')