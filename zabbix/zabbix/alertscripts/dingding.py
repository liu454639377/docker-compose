#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
import os

headers = {'Content-Type': 'application/json;charset=utf-8'}
api_url="https://oapi.dingtalk.com/robot/send?access_token=c194eab8c95e7759e725c58d680f70e4d47674ca34838258bde315b052fd1005xxx"

def msg(text):
    json_text= {
     "msgtype": "markdown",
        "markdown": {
            "title":"钉钉机器人报警",
            "text": text+ 
                   "@xxxxxxxxxxx",
        },
        "at": {
            "atMobiles":[
                "xxxxxxxx",
                "xxxxxxxx",
            ],
            "isAtAll": False,
        }
    }
    print (requests.post(api_url,json.dumps(json_text),headers=headers).content)
    
if __name__ == '__main__':
    text = sys.argv[1]
    msg(text)
