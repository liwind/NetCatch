#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : qsbk.py
# @Author   : Feng
# @Date     : 2017/2/21

import urllib
import urllib2
import re

page = 1
url = "http://www.qiushibaike.com/hot/page/" + str(page)
user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64)"
header = {"User-Agent": user_agent}

try:
    request = urllib2.Request(url, headers=header)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    pattern = re.compile(r'<div.*?author.*?<h2>(.*?)</h2>.*?<div.*?content.*?<span>(.*?)</span>.*?<i.*?number">(.*?)</i>', re.S)
    items = re.findall(pattern, content)
    for item in items:
        print item[0], item[2], "\n",item[1], "\n"
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
