#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : bdtb.py
# @Author: Feng
# @Date  : 2017/2/22
# @Desc  : 爬取百度贴吧的帖子，不要图片

import urllib2
import re


class BDTB:
    def __init__(self, baseUrl, seelz, floorTag):
        self.baseUrl = baseUrl
        self.seelz = '?see_lz=' + str(seelz)
        self.floorTag = floorTag
        self.floor = 0
        self.filename = ''

    # 传入页码，获取该页帖子的HTML代码
    def getPage(self, pageNum):
        try:
            url = self.baseUrl + self.seelz + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print u'状态：网页抓取成功'  #测试
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u'链接百度贴吧失败，错误原因', e.reason
                return None

    # 获取帖子标题
    def getTitle(self, page):
        pattern = re.compile(r'<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            # print u'标题：' + result.group(1)  #测试
            return result.group(1).strip()
        else:
            return None

    # 获取帖子页数
    def getPageSum(self, page):
        pattern = re.compile(r'<span class="red">(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            # print u'页数：' + result.group(1)  #测试
            return result.group(1).strip()
        else:
            return None

    # 处理页面标签，格式化内容
    def strFormat(self, item):
        item = re.sub('<img.*?>|\s{4,7}', '', item)
        item = re.sub('<a.*?>|</a>', '', item)
        item = re.sub('<br><br><br>|<br><br>|<br>', '\n', item)
        item = item.strip()
        return item

    # 传入页面内容,获取每一层楼的内容,
    def getContent(self, page):
        pattern = re.compile(r'<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            content = self.strFormat(item) + '\n'
            contents.append(content.encode('utf-8'))
        return contents

    def setFilename(self, title):
        if title is not None:
            self.filename = title + ".txt"
        else:
            self.filename = u'百度贴吧' + ".txt"

    def writeData(self, file, contents):
        for item in contents:
            self.floor += 1
            if self.floorTag == '1':
                contentTag = '\n' + str(self.floor) + u'楼-----------------------------------------------------------\n'
                file.write(contentTag.encode('utf-8'))
            file.write(item)

    def start(self):
        pageInfo = self.getPage(1)
        pagesum = self.getPageSum(pageInfo)
        title = self.getTitle(pageInfo)
        self.setFilename(title)
        if pagesum == None:
            print u'访问网页出现问题，请重试'
            return
        try:
            print "该帖子共有" + str(pagesum) + "页"
            file = open(self.filename, 'w+')
            file.write(title.encode('utf-8') + '\n')
            for i in range(1, int(pagesum) + 1):
                print "正在写入第" + str(i) + "页数据"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(file, contents)
            file.close()
            # 出现写入异常
        except IOError, e:
            print "写入异常，原因" + e.message
        finally:
            print "写入任务完成"


print u'请输入帖子代号：'
num = raw_input('http://tieba.baidu.com/p/')
baseUrl = 'http://tieba.baidu.com/p/' + str(num)
seelz = raw_input("是否只获取楼主发言，是输入1，否输入0\n")
floorTag = raw_input("是否写入楼层信息，是输入1，否输入0\n")
bdtb = BDTB(baseUrl, seelz, floorTag)
bdtb.start()
