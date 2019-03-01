#coding=utf-8
import wechatsogou
import time
ws_api = wechatsogou.WechatSogouAPI()
ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3)

for i in range(100):
    text = ws_api.search_article('huxiu_com')
    time.sleep(10)
    print '{0}--{1}'.format(i, text)