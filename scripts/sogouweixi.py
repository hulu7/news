#coding=utf-8
import wechatsogou
import time
ws_api = wechatsogou.WechatSogouAPI()
wechatsogou.WechatSogouAPI(proxies={
    "https": "183.129.244.16:19806"
})
test = ws_api.get_gzh_info('huxiu_com')
test2 = 0