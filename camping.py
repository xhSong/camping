# -*- coding: utf-8 -*-
import urllib2
import re
import zlib
from htmldom import htmldom
from datetime import date, timedelta
import calendar
import urllib
from cookielib import CookieJar
from bs4 import BeautifulSoup

site = "https://www.reserveamerica.com"
headers = {
  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
  "Accept-Encoding":"gzip, deflate, br",
  "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,ru;q=0.2,es;q=0.2",
  "Connection":"keep-alive",
  "DNT":"1",
  "Host":"www.reserveamerica.com",
  "Referer":"https://www.reserveamerica.com/",
  "Upgrade-Insecure-Requests":"1",
  "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
}

cookies = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
opener.addheaders = [(k, v) for k, v in headers.items()]

class AvailableSite:
  def __init__(self, campsite_name, site_num, loop_name, date, book_url):
    self.campsite_name = campsite_name
    self.site_num = site_num
    self.loop_name = loop_name
    self.date = date
    self.book_url = book_url

  def __str__(self):
    formatter = '''
  Camping ground name: %s
  Loop name: %s
  Site number: %s
  Available date: %s %s
  Book url: %s
  '''
    return formatter % (self.campsite_name, self.loop_name, self.site_num, self.date, calendar.day_name[self.date.weekday()], self.book_url)

def check(contractCode, parkId, parkName, startDate = date.today(), startIdx = 0):
  params = {
    'calarvdate': startDate.strftime('%m/%d/%Y'),
    'startIdx': startIdx,
    'contractCode': contractCode,
    'parkId': parkId,
    'sitepage':'true',
    'page':'calendar'
  }
  url = site + '/campsiteCalendar.do?' + urllib.urlencode(params)
  # print url
  html = zlib.decompress(opener.open(url).read(), 16+zlib.MAX_WBITS)

  soup = BeautifulSoup(html, 'html.parser')
  body = soup.find('table', id='calendar').find('tbody')
  result = []
  for tr in body.findChildren('tr'):
    if not tr.attrs:
      tds = tr.findChildren('td')
      site_num = tds[0].find('img')['title']
      loop_name = tds[1].find('div', {'class', 'loopName'}).text
      cells = tds[2:]
      for idx, cell in enumerate(cells):
        if 'a' in cell.attrs['class']:
          date = startDate + timedelta(days=idx)
          book_url = site + cell.find('a')['href']
          print site_num, loop_name, date, date.isoweekday(), book_url
          result.append(AvailableSite(parkName, site_num, loop_name, date, book_url))
  return result

def getSiteInfo(contractCode, parkId):
  url = site + '/campsiteCalendar.do?' + urllib.urlencode({'contractCode': contractCode, 'parkId': parkId})
  print url
  'https://www.reserveamerica.com/campsiteCalendar.do?contractCode=NRSO&parkId=70925'
  html = zlib.decompress(opener.open(url).read(), 16+zlib.MAX_WBITS)
  dom = htmldom.HtmlDom().createDom(html)
  total = int(dom.find('span[class=pageresults]').nodeList[0].children[-1].getText())
  sitename = dom.find('span[id=cgroundName]').nodeList[0].getText()
  return {'sitename': sitename, 'sitenum': total}


# check()
def checkNext2Months(contractCode, parkId):
  siteinfo = getSiteInfo(contractCode, parkId)
  print 'there are %d sites in park %s' % (siteinfo['sitenum'], siteinfo['sitename'])
  result = []
  today = date.today()
  for w in range(0, 8, 2):
    for idx in range(0, siteinfo['sitenum'], 25):
      result.extend(check(contractCode, parkId, siteinfo['sitename'], startDate = today + timedelta(weeks=w), startIdx = idx))
  return result