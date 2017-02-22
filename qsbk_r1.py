#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : qsbk_r1.py
# @Author: Feng
# @Date  : 2017/2/22
# @Desc  : 爬取糗事百科的热点段子，不要图片

import urllib2
import re


# 糗事百科爬虫类
class QSBK:
    # 初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64)'
        self.headers = {'User-Agent': self.user_agent}
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        self.enable = False

    # 传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            # 构建请求的request
            request = urllib2.Request(url, headers=self.headers)
            # 利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            # 将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接糗事百科失败,错误原因", e.reason
                return None

    # 传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败...."
            return None
        pattern = re.compile(
            r'<div.*?author.*?<h2>(.*?)</h2>.*?<div.*?content.*?<span>(.*?)</span>.*?<i.*?number">(.*?)</i>', re.S)
        items = re.findall(pattern, pageCode)
        pageStories = []
        for item in items:
            # 抓取故事内容，把它加入list中
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR, "\n", item[1])
            # item[0]是发布者，item[1]是内容，item[2]是点赞数
            pageStories.append([item[0].strip(), text.strip(), item[2].strip()])
        return pageStories

    # 加载并提取页面的内容，加入到列表中
    def loadPage(self):
        # 如果当前页面内容读完，则加载新一页
        if self.enable == True:
            if len(self.stories) < 1:
                # 获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                # 将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    # 获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1

    # 调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            # 每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            # 如果输入Q则程序结束
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t赞:%s\n%s" % (page, story[0], story[2], story[1])

    # 开始方法
    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"
        self.enable = True
        # 先加载一页内容
        self.loadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                nowPage += 1
                self.getOneStory(pageStories, nowPage)


spider = QSBK()
spider.start()
