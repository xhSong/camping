# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from cookielib import CookieJar
from datetime import date, timedelta
import calendar
import urllib
import urllib2
import zlib


SITE = "https://www.reserveamerica.com"

HEADERS = {
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

cookie_jar = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
opener.addheaders = [(k, v) for k, v in HEADERS.items()]


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
    return formatter % (self.campsite_name, self.loop_name, self.site_num, 
        self.date, calendar.day_name[self.date.weekday()], self.book_url)


def check_one_page(contract_code, park_id, park_name, start_date, start_idx):
  sites = []
  try:
    params = {
      'calarvdate': start_date.strftime('%m/%d/%Y'),
      'startIdx': start_idx,
      'contractCode': contract_code,
      'parkId': park_id,
      'sitepage':'true',
      'page':'calendar'
    }
    url = SITE + '/campsiteCalendar.do?' + urllib.urlencode(params)
    html = zlib.decompress(opener.open(url).read(), 16 + zlib.MAX_WBITS)

    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('table', id='calendar').find('tbody')
    for tr in body.findChildren('tr'):
      if not tr.attrs:
        tds = tr.findChildren('td')
        site_num = tds[0].find('img')['title']
        loop_name = tds[1].find('div', {'class', 'loopName'}).text
        cells = tds[2:]
        for idx, cell in enumerate(cells):
          if 'a' in cell.attrs['class']:
            date = start_date + timedelta(days=idx)
            book_url = SITE + cell.find('a')['href']
            print site_num, loop_name, date, date.isoweekday()
            site = AvailableSite(park_name, site_num, loop_name, date, book_url)
            sites.append(site)
  except Exception as e:
    print e
  return sites


def get_park_info(contract_code, park_id):
  try:
    url = SITE + '/campsiteCalendar.do?' + urllib.urlencode(
        {'contractCode': contract_code, 'parkId': park_id})
    print url
    html = zlib.decompress(opener.open(url).read(), 16+zlib.MAX_WBITS)
    soup = BeautifulSoup(html, 'html.parser')
    park_size = int(soup.find('span', {'class':'pageresults'}).findChildren(
        'span')[-1].text)
    park_name = soup.find('span', {'id':'cgroundName'}).text
    return {'name': park_name, 'size': park_size}
  except Exception as e:
    print e
    return {'name': "can't found", 'size': 0}


def check_park_for_n_weeks(contract_code, park_id, weeks = 8):
  park_info = get_park_info(contract_code, park_id)
  print 'There are %d sites in %s.' % (park_info['size'], park_info['name'])
  sites = []
  today = date.today()
  for w in range(0, weeks, 2):
    for idx in range(0, park_info['size'], 25):
      sites.extend(check_one_page(contract_code, park_id, park_info['name'], 
          start_date = today + timedelta(weeks=w), start_idx = idx))
  return sites