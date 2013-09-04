#coding=utf8
__author__ = 'Alexander.Li'
import json
import urllib
import requests

BASE_URL = "https://pcs.baidu.com/rest/2.0/pcs"

FILE_URL = "https://d.pcs.baidu.com/rest/2.0/pcs"

def tou(data, enc='utf8'):
    if isinstance(data, unicode):
        return data
    return data.decode(enc)

def tob(data, enc='utf8'):
    if isinstance(data, unicode):
        return data.encode(enc)
    return data


def urlencode_str(txt):
    return urllib.urlencode({"t":txt})[2:]

class PCS(object):
    def __init__(self, token, base_path="/"):
        self.token = token
        self.bpath = base_path

    def dir(self, name):
        params = dict(method="list", access_token=self.token["access_token"], path="".join([self.bpath,tob(name)]))
        url = "".join([BASE_URL,"/file?",urllib.urlencode(params)])
        r = requests.get(url)
        rs = json.loads(r.text)
        if "error_code" in rs:
            raise Exception, rs
        return rs["list"]

    def films(self, name):
        params = dict(method="list", access_token=self.token["access_token"],type="video", path="".join([self.bpath, tob(name)]))
        url = "".join([BASE_URL, "/stream?", urllib.urlencode(params)])
        r = requests.get(url)
        rs = json.loads(r.text)
        if "error_code" in rs:
            raise Exception, rs
        return rs["list"]


    def url(self, file_name):
        params = dict(method="download", access_token=self.token["access_token"], path=tob(file_name))
        return  "".join([FILE_URL, "/stream?", urllib.urlencode(params)])



    def fetch(self, file_name):
        params = dict(method="streaming", access_token=self.token["access_token"], path=tob(file_name),type="M3U8_854_480")
        url =  "".join([FILE_URL, "/file?", urllib.urlencode(params)])
        #r = requests.get(url, verify=False)
        print url

