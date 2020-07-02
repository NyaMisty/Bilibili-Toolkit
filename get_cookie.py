import os
import sys
oristdout = sys.stdout
f = open(os.devnull, 'w')
sys.stdout = f

import toml
from queue import Queue
from bilibili import Bilibili
import requests


config_file = "config.toml"
try:
    with open(config_file, "r", encoding='utf-8') as f:
        config = toml.load(f)
except:
    print(f"Can't open {config_file}")
    raise
accounts = []
for line in config['user']['account'].splitlines():
    try:
        if line[0] == "#":
            continue
        pairs = {}
        for pair in line.strip(";").split(";"):
            if len(pair.split("=")) == 2:
                key, value = pair.split("=")
                pairs[key] = value
        password = all(key in pairs for key in ["username", "password"])
        token = all(key in pairs for key in ["access_token", "refresh_token"])
        cookie = all(key in pairs for key in ["bili_jct", "DedeUserID", "DedeUserID__ckMd5", "sid", "SESSDATA"])
        if password or token or cookie:
            accounts.append(pairs)
    except:
        pass

config['user'].pop("account")

instance = Bilibili(config['global']['https'], Queue())
instance.login(force_refresh_token=False, **accounts[0])

sys.stdout = oristdout
print(requests.cookies.get_cookie_header(instance._session.cookies, requests.Request('GET', 'https://www.bilibili.com')))