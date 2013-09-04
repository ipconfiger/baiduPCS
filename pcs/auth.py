#coding=utf8
__author__ = 'Alexander.Li'

import urllib
import requests
import json

BASE_URL = "https://openapi.baidu.com/oauth/2.0"

class Authenticator(object):
    def __init__(self, AppKey, AppSecret, scope):
        self.appkey = AppKey
        self.appsecret = AppSecret
        self.scope = scope

    def device_code(self):
        params = dict(client_id=self.appkey,response_type="device_code",scope=self.scope)
        url = "".join([BASE_URL,"/device/code?",urllib.urlencode(params)])
        r = requests.get(url)
        return json.loads(r.text)

    def device_token(self, code_object):
        code = code_object["device_code"]
        params = dict(grant_type="device_token", code=code, client_id=self.appkey, client_secret=self.appsecret)
        url = "".join([BASE_URL,"/token?", urllib.urlencode(params)])
        r = requests.get(url)
        return json.loads(r.text)


    def code(self, scope="basic,netdisk"):
        params = dict()
        url =  "".join([BASE_URL,"/code?",urllib.urlencode(params)])


    def refresh(self, token):
        if token["expires_in"]<10:
            params = dict(grant_type="refresh_token", refresh_token=token["refresh_token"], client_id=self.appkey, client_secret=self.appsecret, scope=self.scope)
            url="".join([BASE_URL,"/token?",urllib.urlencode(params)])
            r = requests.get(url)
            return json.loads(r.text)
        return None

    def show_code(self, code_url):
        import requests
        import Image
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile() as f:
            f.write(requests.get(code_url).content)
            f.seek(0)
            img = Image.open(f.name)
            img.show()


if __name__=="__main__":
    auth = Authenticator("9WTPqAjjsly8QarWLlaMzjXA", "IBZBQhhUt3xmZ67AlXAHnhgVTp1hLLGe", "basic,netdisk")
    code = auth.device_code()
    code_url = code["qrcode_url"] if "qrcode_url" in code else None
    if code_url:
        print code_url
        auth.show_code(code_url)
        raw_input("...any key to continue")
        token = auth.device_token(code)
        print token
        from api import PCS
        print "\n\n\n\n\n\n\n\n\n\n"
        pcs = PCS(token)
        for fileinfo in pcs.films(u"apps/panBox"):
            print pcs.fetch(fileinfo["path"])
    else:
        print code