import json
import urllib.request
import urllib.parse
import os
import requests
import time
import re


'''
LANGUAGES = {
    'zh-CN': 'chinese_simplified',
    'zh-TW': 'chinese_traditional',
    'en': 'english',
    'fr': 'french',
    'es': 'spanish',
  }
'''

class BingTrans:

    def __init__(self): 
        #, token = 'G3ZWjaCMlRWpU3XmNbsqgO_orFU_t3cA', key = '1642568801733', ig = 'F2755F0C030D4B10B4CA4F719EF5C5FB', start_IID = 3):
        #获取ig，后来发现ig要跟token和key配合使用才行
        # header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'}
        # response = requests.get('https://cn.bing.com/translator/', headers=header)
        # ig = re.search(',IG:"(.*?)",', response.text).group(1)
                        
        self.token = 'fS6i_FtrWOblPQtWtyJU5oM_7rHFoDPK'
        self.key = '1642586407010'
        agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        ig = '318F6D3CD85F487FA2A4E56D1D6B7DEC'
        start_IID = 7

        #请求地址
        self.url = 'https://cn.bing.com/ttranslatev3?isVertical=1&&IG=%s&IID=translator.5023.%d' % (ig, start_IID)       
        #伪装成的浏览器信息, 必须加cookie才能提高稳定性和成功率
        self.headers = {
            'User-Agent':'%s' % agent,
            'referer':'https://cn.bing.com/translator',            
            'origin': 'https://cn.bing.com',
            'cookie': 'SUID=M; MUID=0817E7C7DFA06F992C9EF6F6DEEA6E16; MUIDB=0817E7C7DFA06F992C9EF6F6DEEA6E16; _EDGE_V=1; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=D879E98907D049798EC9D94DEB32AC94&dmnchg=1; btstkn=qZNE6G20%2FIZtTJ8NvEro31NUixCVgDOEPV773IoeDTkDDmG5%2FevAEicckt%2Fl2RfErrmq8b70%2B3j0AWkzenBJhOkPpzEWdTmZO%2BcoZquZVs8%3D; _TTSS_OUT=hist=WyJlbiIsImFmIiwiZnIiXQ==; _tarLang=default=fr; _EDGE_S=SID=3FE8DE64CC50687F0A55CF55CD366977; _SS=SID=3FE8DE64CC50687F0A55CF55CD366977; SRCHUSR=DOB=20220119&T=1642586407000&TPC=1642578783000; SRCHHPGUSR=SRCHLANG=zh-Hans&HV=1642586407&WTS=63778183207; ipv6=hit=1642590007798&t=4; SNRHOP=I=&TS=; _TTSS_IN=hist=WyJmciIsImFmIiwiZW4iLCJhdXRvLWRldGVjdCJd',
        }


    def translate(self, text, fromlang='en', tolang='fr'):
        #设置请求参数
        self.fromlang = fromlang
        self.tolang = tolang
        post_data={'fromlang':'%s' % self.fromlang, 'text':'%s' % text, 'to':'%s' % self.tolang, 'token':'%s' % self.token, 'key':'%s' % self.key} #
        data = {}
        while isinstance(data, dict): #翻译失败之后，返回字典，成功返回json
            result = requests.post(self.url, headers = self.headers, data=post_data).content.decode() #发出请求并将请求数据转换为str格式
            data = json.loads(result) #将字符串转化为Python的列表和字典
            time.sleep(0.1)

        translate_to = data[0]['translations'][0]['text'] #从转化的数据中获取翻译文本
        
        if tolang == 'fr':
            translate_to = translate_to.replace(' »', '"')
            translate_to = translate_to.replace(' »', '"')
            translate_to = translate_to.replace('« ', '"')
            translate_to = translate_to.replace('« ', '"')
            translate_to = translate_to.replace('LANG_ENGLISH LINGUISTIQUE, SUBLANG_ENGLISH_US', 'LANGUAGE LANG_FRENCH, SUBLANG_FRENCH')
            translate_to = translate_to.replace('LANG_CHINESE DE LANGUE, 0x2', 'LANGUAGE LANG_FRENCH, SUBLANG_FRENCH')
            #translate_to = translate_to.replace('".\n', '."\n')

        print('translate from: %s to: %s' % (text, translate_to))

        return translate_to


    #翻译一个文件
    def translateOneFile(self, fromlang='en', tolang='fr', s_fromfile='', s_tofile='', encode_from = 'utf-8', encode_to = 'utf-8'):       
        if os.path.exists(s_tofile): #已经创建过的旧不再创建了
            return

        print('Traslate: %s to: %s' % (s_fromfile, s_tofile))

        s_lines = []
        with open(s_fromfile, 'r', encoding=encode_from, errors='ignore' ) as f:
            s_lines = f.readlines()

        s_to_trans = ''
        with open(s_tofile, 'w', encoding=encode_to, errors='ignore' ) as f:
            for s_line in s_lines:
                s_text = str(s_line)
                if len(s_to_trans) + len(s_text) >= 800:                                
                    s_text_to = self.translate(s_to_trans, fromlang, tolang)                                
                    f.write(s_text_to)
                    s_to_trans = s_text
                else:
                    s_to_trans += s_text

            if len(s_to_trans) > 0: #最后剩余的部分
                s_text_to = self.translate(s_to_trans, fromlang, tolang) 
                f.write(s_text_to)



#Testing
if __name__ == '__main__' :
    translate = BingTrans()
    result = translate.translate('I have a book', 'en', 'fr')
    print(result)


