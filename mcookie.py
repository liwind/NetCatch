#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : mcookie.py
# @Author   : Feng
# @Date     : 2017/2/21

import urllib
import urllib2
import cookielib

filename = "cookie.txt"
loginurl = "http://www.imooc.com/"
value = {"username":"liwind93@qq.com", "password":"lifeng1993526"}

data = urllib.urlencode(value)
#定义cookie变量
cookie = cookielib.MozillaCookieJar(filename)
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
response = opener.open(loginurl, data)
#保存cookie到本地
cookie.save(ignore_discard=True, ignore_expires=True)
print response.read()