#!/usr/bin/env python
# coding: utf-8

import os
import time
import urllib.request
import configparser

config = configparser.ConfigParser()

config.read('clash-update.ini')

base_str = str()
for key in config['SETTINGS']:
    base_str = base_str + "{}: {}\n".format(key, config['SETTINGS'][key])
base_str = base_str + "\n\n"

url_req = urllib.request.Request(config["PROVIDER"]["URL"])
url_req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                   Chrome/87.0.4280.141 Safari/537.36')
while True:
    try:
        response = urllib.request.urlopen(url_req, timeout=10)
        print("{} Download config success.".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        con = response.read().decode('utf-8')
        num = con.index("proxies:")
        print("{} Process config success.".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        f = open('config.yaml', 'w')
        f.write(base_str)
        f.write(con[num:])
        f.close()
        print("{} Save config success.".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        cmd = os.system("""
        wget --no-check-certificate --quiet --method PUT \
              --timeout=5 \
              --header 'Authorization: Bearer """ + config["SETTINGS"]["SECRET"] + """' \
              --header 'Content-Type: application/json' \
              --body-data '{"path": "/root/.config/clash/config.yaml"}' '""" + config["SETTINGS"]["URL"] + """/configs'
        """)
        if cmd == 0:
            print(
                "{} Restart docker container success: {}.".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                                  config["CONTAINER"]["NAME"]))
        else:
            print("{} Restart docker container failed: {}.".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                                   cmd))
        response.close()
    except Exception as e:
        print(e)
    print("{} Sleep for {}s".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                    config["PROVIDER"]["UPDATEINTERVAL"]))
    time.sleep(int(config["PROVIDER"]["UPDATEINTERVAL"]))
