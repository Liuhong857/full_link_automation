# -*- coding:utf-8 -*-
# author:liuhong
import requests,json
import urllib3

class RunMain():
    def __init__(self,url,method,data=None,headers=None,verify=None):
        self.t=self.runmain(url,method,data,headers,verify)

    def send_post(self,url,data,headers,verify=False):
        r = requests.post(url=url,data=data,headers=headers,verify=False)
        self.result= r.json()
        self.code = r.status_code
        return json.dumps(self.result,indent=2,sort_keys=False,ensure_ascii=False)
    def send_get(self,url,data,headers,verify=False):
        r = requests.get(url=url,params=data,headers=headers,verify=False)
        self.result =r.json()
        self.code= r.status_code
        return json.dumps(self.result, indent=2, sort_keys=False, ensure_ascii=False)
    # 利用json.dumps将响应数据进行json格式的编码解析
    # indent=2将输出结果缩进2个字符显示
    # sort_keys=False，输出结果是否按照关键字排序
    # json.dumps 序列化时对中文默认使用的ascii编码，ensure_ascii=False才会输出中文
    # return result
    def runmain(self,url, method, data=None, headers=None, verify=False):
        print(method)
        if method=='GET':
            r = self.send_get(url, data, headers, verify=False)
        else:
            r = self.send_post(url, data, headers, verify=False)
        return r