#!/usr/bin/env python
# coding: utf-8
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
import hashlib
import numpy as np
import time
import hashlib
import tkinter as tk
from pdf_extractor import extract_pdf_content
import threading
from tkinter import messagebox
from tkinter.filedialog import *
#翻译程序
def fanyi(content):
    
    appid = entry_uname.get()
    secretKey = entry_upwd.get()
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
#提取PDF内容翻译并存取

def translate():
    btn_start.config(state=tk.DISABLED)
    
    pdfs =glob.glob('{}/*.pdf'.format(entry_pdf.get()))
    for pdf in pdfs:
        con = extract_pdf_content(pdf)
        var5.set(pdf)  
       
        con=con.encode('gbk', 'ignore').decode('gbk')
        c = con.replace('\n','')
        c = re.sub('\s+',' ',c)
        pattern=re.compile(r'(?<=\]|\))\.(?=\s[A-Z])')
        d=c
        d=pattern.sub('.\n',d)
        d=re.sub(r'\.\s(?=\[)','. \n',d)
        d=re.sub(r'(?<=\w{3})\.(?=\s[A-Z])','.\n',d)
        m=re.split(r'\n',d)
        t=entry_txt.get()         
        txt_file = open(t, 'a+',encoding='UTF-8')  # 以写的格式打开先打开文件
        txt_file.write('\n'+'\n'+'\n'+pdf+'\n'+'\n'+'\n')
        for i in m:
        
            var6.set(i)
            time.sleep(1)
            i=i.encode('ISO-8859-1', 'ignore')#.decode()
            i=i.decode('utf-8','ignore')
            i=str(i)
            txt_file.write(i)
            i=str(i)
            b=fanyi(i)
            b=str(b)
            var7.set(b)
            txt_file.write(b)
        txt_file.close()
    tk.Label(window,text='Completed').place(x=100,y=350)
    
        
# 点击“选择文件”按钮调用该功能
def selectFilePath():
    path_ = askopenfilename(title='选择文件')
    
    var4.set(path_)
# 点击“选择文件夹”调用该功能
def selectDirecPath():
    path_ = askdirectory(title='选择文件夹')
    var3.set(path_)
    
    
window = tk.Tk()
window.title('这是一个可将PDF内容转换为Txt并翻译的软件')
window.geometry('500x400')


var1=tk.StringVar()
var1.set('20191107000354292')
var2=tk.StringVar()
var2.set('thY2vGYgTKROz1q55Y8c')
var3=tk.StringVar()
var3.set('E:/pdf')
var4=tk.StringVar()
var4.set('E:/pdf/ik.txt')

tk.Label(window,text='请输入百度翻译API账号:').place(x=29,y=20)
entry_uname = tk.Entry(window,width=25,textvariable=var1)
entry_uname.place(x=200,y=20)

tk.Label(window,text='请输入百度翻译API密码：').place(x=29,y=50)
entry_upwd = tk.Entry(window,width=25,textvariable=var2)
entry_upwd.place(x=200,y=50)


tk.Label(window,text='请输入PDF文件地址：').place(x=50,y=80)
entry_pdf = tk.Entry(window,width=25,textvariable=var3)
entry_pdf.place(x=200,y=80)
# 输入文件一行
btn_pathin1 = tk.Button(window, text='选择文件夹',width=10, command=selectDirecPath).place(x=400, y=80)  # 按钮

tk.Label(window,text='请输入Txt文件地址：').place(x=52,y=110)
entry_txt = tk.Entry(window,width=25,textvariable=var4)
entry_txt.place(x=200,y=110)
btn_pathin2 = tk.Button(window, text='选择文件', width=10,command=selectFilePath).place(x=400, y=110)  # 按钮
#输出内容
var5=tk.StringVar()
var6=tk.StringVar()
var7=tk.StringVar()
tk.Label(window,text='正在翻译：').place(x=35,y=200)
tk.Label(window,textvariable=var5,width=45,height=2,wraplength = 350,justify = 'left').place(x=100,y=200)
tk.Label(window,text='英文：').place(x=60,y=250)
tk.Label(window,textvariable=var6,width=45,height=1).place(x=100,y=250)
tk.Label(window,text='中文：').place(x=60,y=300)
tk.Label(window,textvariable=var7,width=45).place(x=100,y=300)

    
def thread_it(func, *args):
    # 创建线程
    t = threading.Thread(target=func, args=args)
    # 守护线程
    t.setDaemon(True)
    # 启动
    t.start()
    
btn_start=tk.Button(window,text='Start',width=20,command=lambda:thread_it(translate))
btn_start.place(x=150,y=150)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)


window.mainloop()






