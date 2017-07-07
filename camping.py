# -*- coding: utf-8 -*-
import urllib2
import re
import zlib
from htmldom import htmldom
from datetime import date, timedelta
import urllib


site = "https://www.reserveamerica.com/campsiteCalendar.do?%s"

headers = {
  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
  "Accept-Encoding":"gzip, deflate, br",
  "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,ru;q=0.2,es;q=0.2",
  "Connection":"keep-alive",
  "Cookie": "_rauv_=F89CD76B341F0EA0FB8D4F264B1C2081.awolvprodweb14_; _rauv_=F89CD76B341F0EA0FB8D4F264B1C2081.awolvprodweb14_; JSESSIONID=BDA53143B26CDD150D8AF1511BD42EF6.awolvprodweb09; utag_main=v_id:015d1166c9cf00081822c023f71504079006c07100838$_sn:3$_ss:0$_st:1499417079282$vapi_domain:reserveamerica.com$ses_id:1499406840733%3Bexp-session$_pn:42%3Bexp-session; _ga=GA1.2.216199597.1499235535; _gid=GA1.2.481497827.1499235535; _gat=1; s_cc=true; s_fid=2620173E18ECF0E3-09875CF377873DD5; s_sq=anreserveamericaprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dreserveamerica%25253Acampground%252520details%2526link%253DNext%2525202%252520weeks%252520%25253E%2526region%253Dcalendar%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dreserveamerica%25253Acampground%252520details%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.reserveamerica.com%25252FcampsiteCalendar.do%25253Fpage%25253Dmatrix%252526calarvdate%25253D08%25252F18%25252F2017%252526contractCode%25253DCA%2526ot%253DA; NSC_MWQSPE-VXQ-IUUQT=ffffffff09d44f0c45525d5f4f58455e445a4a422141",
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

def check(startDate = date.today(), startIdx = 0):
  params['calarvdate'] = startDate.strftime('%m/%d/20%y')
  params['startIdx'] = startIdx
  url = site % (urllib.urlencode(params))
  print url
  request = urllib2.Request(url, None, headers)
  response = urllib2.urlopen(request)
  print type(response.headers['Set-Cookie']), response.headers['Set-Cookie']
  html = zlib.decompress(response.read(), 16+zlib.MAX_WBITS)
  dom = htmldom.HtmlDom().createDom(html)
  table = dom.find("table[id=calendar]")
  print [th.getText() for th in table.find("thead > tr > th").nodeList]
  for line in table.find("tbody > tr").nodeList:
    if not line.attributes:
      sitenum = line.children[0].getText()
      for idx, cell in enumerate(line.children[2:]):
        if 'class' in cell.attributes and 'a' in cell.attributes['class']:
          print (startDate + timedelta(days=idx)).strftime('%m/%d/%y')

check()

# today = date.today()
# for w in range(0, 20, 2):
#   for idx in [0, 25, 50]:
#     check(startDate = today + timedelta(weeks=w), startIdx = idx)
