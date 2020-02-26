#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# author: Friday
import urllib.request
import http.cookiejar
import urllib.parse
import gzip
import time
import json
import os


def ungzip(data):
    try:        # unzip data
        data = gzip.decompress(data)
    except:
        pass
    return data

# deal with cookies
cj = http.cookiejar.CookieJar()


def getOpener(head):
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener


def sign(username, password):
    url = 'http://www.rrys2019.com/'
    header = {
        'Accept': 'application/json, text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73'
                      ' Safari/537.36',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'}
    opener = getOpener(header)
    try:
        op = opener.open(url)
    except:
        print("Can't open 'http://www.rrys2019.com', please check your connection")
        return False
    url += 'User/Login/ajaxLogin'
    postDict = {
        'account': username,
        'password': password,
        'remember': 1,
        'url_back': 'http://www.rrys2019.com/'
    }
    postData = urllib.parse.urlencode(postDict).encode()
    op = opener.open(url, postData)
    data = op.read()
    data = ungzip(data)
    data = json.loads(data.decode('utf-8'))
    print(data)
    if data['status'] != 1:
        print('wrong username or password, login error')
        return False
    print(data['info'])
    return True

if __name__ == '__main__':
    username = os.getenv('USERNAME')
    passwd = os.getenv('PASSWD')
    if sign(username, passwd):
        print('成功!')