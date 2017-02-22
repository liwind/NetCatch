#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : mhtmlparser.py
# @Author   : Feng
# @Date     : 2017/2/21

import urllib2
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print('<%s>' % tag)

    def handle_endtag(self, tag):
        print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('<%s/>' % tag)

    def handle_data(self, data):
        print('data')

    def handle_comment(self, data):
        print('<!-- -->')

    def handle_entityref(self, name):
        print('&%s;' % name)

    def handle_charref(self, name):
        print('&#%s;' % name)



page = 1
url = "http://www.qiushibaike.com/hot/page/" + str(page)
user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64)"
header = {"User-Agent": user_agent}

try:
    request = urllib2.Request(url, headers=header)
    response = urllib2.urlopen(request)

except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason

parser = MyHTMLParser()
parser.feed(response.read())