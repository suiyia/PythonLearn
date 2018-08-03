from googletrans import Translator
import hashlib
import json
import urllib
import random
import codecs
import http.client
from hashlib import md5
from urllib.parse import quote
import http.client as httplib

# 谷歌翻译
def googletrans(str): 
    translator = Translator(service_urls=[
        'translate.google.cn'
    ])
    return translator.translate(str,'zh-cn').text

# 有道翻译
# def youdao(str1): 
#     appKey = '425e1a93c9402146'
#     secretKey = 'xdeA7RLjEpjRIiee6U7z6iWJvUIte4m8'
#     myurl = '/api'
#     q = str1
#     fromLang = 'EN'
#     toLang = 'zh-CHS'
#     salt = random.randint(1, 65536)
#     sign = appKey + q + str(salt) + secretKey
#     m1 = hashlib.md5()
#     m1.update(sign.encode(encoding='utf-8'))
#     sign = m1.hexdigest()
#     myurl = myurl + '?appKey=' + appKey + '&q=' + urllib.parse.quote(
#         q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
#         salt) + '&sign=' + sign
#     httpClient = http.client.HTTPSConnection('openapi.youdao.com')
#     httpClient.request('GET', myurl)
#     response = httpClient.getresponse().read().decode('utf-8')
#     a = json.loads(response)
#     return (a['translation'])

def baidu(str1): 
    try:
        appid = '20170519000048437'
        secretKey = 'ahaw9Gw0LK_RD27cSg6S'  
        myurl = '/api/trans/vip/translate'
        fromLang = 'en'
        toLang = 'zh'
        salt = random.randint(32768, 65536)
        sign = appid + str1 + str(salt) + secretKey
        m1 = md5()
        m1.update(sign.encode('utf-8'))
        sign = m1.hexdigest()
        myurl = myurl+'?appid='+appid+'&q='+quote(str1)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        res = response.read()
        content = json.loads(res)
        trans_result = content['trans_result']
    except KeyError:
        code = content['error_code']
        if code == 52001:
            print("①TIMEOUT：超时（52001）【请调整文本字符长度】")
        elif code == 52002:
            print('②SYSTEM ERROR：翻译系统错误（52002）')
        elif code == 52003:
            print("③UNAUTHORIZED USER：未授权的用户（52003）【请检查是否将api key输入错误")
        else:
            print('③msg:PARAM_FROM_TO_OR_Q_EMPTY：必填参数为空（5004）【from 或 to 或query 三个必填参数，请检查是否相关参数未填写完整】')
        return
    str2 = ''
    if trans_result != 'None':
        for i in range(0, len(trans_result)):
            str2 += trans_result[i]['dst']
    else:
        print('baidu trans_result None')
    return str2    
