import urllib
import urllib2
import cookielib


url = "http://blog.csdn.net/cqcre"
request = urllib2.Request(url)
try:
    #访问网页并返回html代码
    response=urllib2.urlopen(request)
    print response.read()
except urllib2.HTTPError, e:
    print e.code
    print e.reason