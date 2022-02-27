import json
import urllib.request
import urllib.parse
import os
from HandleJs import Py4Js
import requests


def open_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read().decode('utf-8')
    return data


def buildUrl(content, tk, tl):
    baseUrl = 'http://translate.google.cn/' #translate_a/single'
    baseUrl += '?client=t&'
    baseUrl += 'sl=auto&'
    baseUrl += 'tl=' + str(tl) + '&'
    baseUrl += 'hl=zh-CN&'
    baseUrl += 'dt=at&'
    baseUrl += 'dt=bd&'
    baseUrl += 'dt=ex&'
    baseUrl += 'dt=ld&'
    baseUrl += 'dt=md&'
    baseUrl += 'dt=qca&'
    baseUrl += 'dt=rw&'
    baseUrl += 'dt=rm&'
    baseUrl += 'dt=ss&'
    baseUrl += 'dt=t&'
    baseUrl += 'ie=UTF-8&'
    baseUrl += 'oe=UTF-8&'
    baseUrl += 'clearbtn=1&'
    baseUrl += 'otf=1&'
    baseUrl += 'pc=1&'
    baseUrl += 'srcrom=0&'
    baseUrl += 'ssel=0&'
    baseUrl += 'tsel=0&'
    baseUrl += 'kc=2&'
    baseUrl += 'tk=' + str(tk) + '&'
    baseUrl += 'op=translate&'
    baseUrl += 'q=' + content
    return baseUrl


def translate(data, tk, tl):  
    #content是要翻译的内容
    content = urllib.parse.quote(data[1])
    url = buildUrl(content, tk, tl)

    result = open_url(url)
    print(result)
    with open(r'D:\Working\WeeklyWorking\0ThisWeek\a.txt', 'w', encoding='utf-8') as f:
        f.write(result)

    res_json = json.loads(result)
    trans_text = res_json[0][0][0]
    #去除读取文字中前后的换行符和逗号及单引号或双引号
    original = data[1].strip("\n").strip(",").strip("'").strip('"')
    translate = trans_text.strip(",").strip("'").strip('"')
    print(original + " : " + translate)
    result = data[0] + ": " + trans_text + "\n"
    return result
    #保存翻译后的内容到文件中
    #with open('/home/wuzhangwei/python/english.en.js', 'a', encoding='utf-8') as f:
    #    f.write(result)
 

def main():
    js = Py4Js()
    #tl是要翻译的目标语种，值参照ISO 639-1标准，如果翻译成中文"zh/zh-CN简体中文"
    tl = "en"
    #读取需要翻译的文件
    with open('/home/wuzhangwei/python/chinese.zh.js', encoding= "utf-8") as file_obj:
        for line in file_obj:
            data = line.split(":",1)
            if len(data) == 2:
                tk = js.getTk(data[1])
                translate(data, tk, tl)
            else:
                print("Illegal row data")           
    

if __name__ == "__main__":
    #main()
    # js = Py4Js()
    # source = '我有点笨'
    # tl = "en"
    # tk = js.getTk(source)
    # dest = translate(source, tk, tl)
    # print(dest)
    
    #百度    
    # url = 'https://fanyi.baidu.com/v2transapi?from=zh&to=fra'
    # data = {
    #     'from': 'zh',
    #     'to': 'fra',
    #     'query': '我有点笨',
    #     'simple_means_flag': '3',
    #     'sign': '626851.881554',
    #     'token': 'df740c8f1a1413effc12369733ebd1e7',
    #     'domain': 'common'
    # } 
    # res = requests.post(url, data=data).json()
    # print(res)
    # print(res['data'][0]['dst'])

    #有道-只支持中英文
    # url0 = 'https://fanyi.youdao.com/ctlog?pos=undefined&action=&sentence_number=1&type=zh-CHS2fr'
    # res = requests.get(url0)
    # print(res)

    # url = 'http://fanyi.youdao.com/translate'
    # url = 'https://fanyi.youdao.com/translate'#_o?smartresult=dict&smartresult=rule'
    # data = {
    #     "i": "我有点笨",  # 待翻译的字符串
    #     #"i": "I have a book.", 
    #     "from": "zh-CHS",
    #     "to": "fr",
    #     "smartresult": "dict",
    #     "client": "fanyideskweb",
    #     "salt": "16424909729540",
    #     "sign": "e29819ab7270f0161b6adab92b2a373a",
    #     "lts": "1642490972954",
    #     "bv": "3c2c16e00dc6f2c6dfe859fcd6ef9592",
    #     "doctype": "json",
    #     "version": "2.1",
    #     "keyfrom": "fanyi.web",
    #     "action": "lan-select"
    # }
    # res = requests.post(url, data=data).json()
    # print(res)
    # print(res['translateResult'][0][0]['tgt'])  # 打印翻译后的结果


    #bing
    url='https://cn.bing.com/ttranslatev3?isVertical=1&&IG=82F0D12B9EB44DC38DF2A15A64F37A04&IID=translator.5022.7' #请求地址
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'} #设置请求头
    post_data={'fromlang':'zh-Hans','text':'我有点笨','to':'fr','token':'CeRLWhaWX5A88_jvPC2kTaoJ-LyPsuk5','key':'1642494372023'} #设置请求参数
    result=requests.post(url,headers=headers, data=post_data).content.decode() #发出请求并将请求数据转换为str格式
    print(result)
    data=json.loads(result) #将字符串转化为Python的列表和字典
    translate_text=data[0]['translations'][0]['text'] #从转化的数据中获取翻译文本
    print(translate_text)
 