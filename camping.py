# -*- coding: utf-8 -*-
import urllib2
import re
import zlib
from htmldom import htmldom
from datetime import date, timedelta
import urllib
from cookielib import CookieJar

site = "https://www.reserveamerica.com/campsiteCalendar.do?%s"
headers = {
  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
  "Accept-Encoding":"gzip, deflate, br",
  "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,ru;q=0.2,es;q=0.2",
  "Connection":"keep-alive",
  "DNT":"1",
  "Host":"www.reserveamerica.com",
  "Referer":"https://www.reserveamerica.com/camping/half-moon-bay-sb/r/campgroundDetails.do?contractCode=CA&parkId=120039",
  "Upgrade-Insecure-Requests":"1",
  "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
}

params = {
  "page":"calendar",
  "contractCode":"CA",
  "parkId":120039,
  "calarvdate":"11/09/2017",
  "sitepage":"true",
  "startIdx":0
}
cookies = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
opener.addheaders = [(k, v) for k, v in headers.items()]

def check(startDate = date.today(), startIdx = 0):
  params['calarvdate'] = startDate.strftime('%m/%d/20%y')
  params['startIdx'] = startIdx
  url = site % (urllib.urlencode(params))
  print url
  html = zlib.decompress(opener.open(url).read(), 16+zlib.MAX_WBITS)
  dom = htmldom.HtmlDom().createDom(html)
  table = dom.find("table[id=calendar]")
  print [th.getText() for th in table.find("thead > tr > th").nodeList]
  for line in table.find("tbody > tr").nodeList:
    if not line.attributes:
      sitenum = line.children[0].getText()
      for idx, cell in enumerate(line.children[2:]):
        if 'class' in cell.attributes and 'a' in cell.attributes['class']:
          print (startDate + timedelta(days=idx)).strftime('%m/%d/%y')

# check()

today = date.today()
for w in range(0, 20, 2):
  for idx in [0, 25, 50]:
    check(startDate = today + timedelta(weeks=w), startIdx = idx)
