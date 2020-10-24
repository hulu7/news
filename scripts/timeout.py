#coding:utf-8
import time
import eventlet #导入eventlet这个模块
eventlet.monkey_patch() #必须加这条代码
with eventlet.Timeout(2, False): #设置超时时间为2秒
  time.sleep(1)
  print('没有跳过这条输出')
print('跳过了输出')