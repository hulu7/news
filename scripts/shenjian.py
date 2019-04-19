# -*- coding: utf-8 -*-

import requests

weixinId="Sanlihe1"

appid="137dddef7b95cffaee7e3cf870295b2b"

url = "https://api.shenjian.io/?appid="+appid+"&weixinId="+weixinId

request = requests.get(url)
print requests
print requests