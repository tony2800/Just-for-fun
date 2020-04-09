#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import urllib.request  
import urllib.parse  
import json 
import http.client
import cgi
from html.parser import HTMLParser
import re
import glob
import os
import codecs
#from BaiduTranslate2 import fanyi
import hashlib
import numpy as np
import time
import hashlib



# In[2]:
a=input('请输入百度翻译API账号(如果没有请直接按enter键跳过):')
if a == '':
    a = '20191107000354292'
s=input('请输入百度翻译API密码(如果没有请直接按enter键跳过):')
if s == '':
    s = 'thY2vGYgTKROz1q55Y8c'
pdf_path = input('请输入源文件pdf路径:')
txt_path = input('请输入输出txt文件路径:')


def fanyi(content):
    
    appid = a
    secretKey = s
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content
    fromLang = 'en'  # 源语言
    toLang = 'zh'  # 翻译后的语言
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")  # 获得返回的结果，结果为json格式
        js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构
        dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
        return  dst+'\n'
    except Exception as e:
        print(e)
        
    finally:
        if httpClient:
            httpClient.close()


# In[3]:





# In[4]:


pdfs = glob.glob("{}/*.pdf".format(pdf_path))


# In[5]:


pdfs


# In[6]:


from pdf_extractor import extract_pdf_content


# In[7]:


for pdf in pdfs:
    con = extract_pdf_content(pdf)  
    print("Extracting content from {} ...".format(pdf))
    #con=con.encode('utf-8')
    con=con.encode('gbk', 'ignore').decode('gbk')
    c = con.replace('\n','')
    c = re.sub('\s+',' ',c)
    pattern=re.compile(r'(?<=\]|\))\.(?=\s[A-Z])')
    d=c
    d=pattern.sub('.\n',d)
    d=re.sub(r'\.\s(?=\[)','. \n',d)
    d=re.sub(r'(?<=\w{3})\.(?=\s[A-Z])','.\n',d)
    m=re.split(r'\n',d) 
    txt_file = open(txt_path, 'a+',encoding='UTF-8')  # 以写的格式打开先打开文件
    txt_file.write(pdf+'\n'+'\n'+'\n')
    for i in m:
        #txt_file.write(i+'\n')
        #i=i.encode(encoding='utf-8', errors='backslashreplace')
        #txt_file.write("{},{}".format(i,fanyi(i))+'\n')
        #i = i.encode('utf-8','ignore')
        time.sleep(1)
        i=i.encode('ISO-8859-1', 'ignore')#.decode()
        i=i.decode('utf-8','ignore')
        i=str(i)
       # i=i.decode(encoding='utf-8',errors='ignore')#bytes.decode(i,'ignore')
        txt_file.write(i)
        i=str(i)
        b=fanyi(i)
        b=str(b)
        txt_file.write(b)
    txt_file.close()   


# In[ ]:





# In[ ]:




