import scrapy
import re

from tides.items import TidesItem

class TidesSpider(scrapy.Spider):
  name = "tides"
  allowed_domains = ["tides.gc.ca"]
  start_urls = [
    'http://tides.gc.ca/eng/'
  ]
  
  # region
  # select#mapSelect > option 
  # http://tides.gc.ca/eng/find/region?id=5
  def parse(self, response):
    for region in response.xpath('//option'):
      value = region.xpath('@value').extract()[0]
      name = region.xpath('text()').extract()[0]
      url = "http://tides.gc.ca/eng/find/zone?id=%s" % value
      # print value, name, url
      yield scrapy.Request(url, callback=self.parse_second_level)

  # zone 
  # select#mapSelect > option 
  # http://tides.gc.ca/eng/find/zone?id=22
  def parse_second_level(self, response):
    # 7 day increments
    start_dates = [
      [1,1],[1,8],[1,15],[1,22],[1, 29],
      [2,5],[2,12],[2,19],[2,26],
      [3,5],[3,12],[3,19],[3,26],
      [4,2],[4,9],[4,16],[4,30],
      [5,7],[5,14],[5,21],[5,28],
      [6,4],[6,11],[6,18],[6,25],
      [7,2],[7,9],[7,16],[7,23],[7,30],
      [8,6],[8,13],[8,20],[8,27],
      [9,3],[9,10],[9,17],[9,24],
      [10,1],[10,8],[10,15],[10,22],[10, 29],
      [11,5],[11,12],[11,19],[11,26],
      [12,3],[12,10],[12,17],[12,24],[12,31]
    ]

    for zone in response.xpath('//option'):
      sid = zone.xpath('@value').extract()[0]
      for date in start_dates:
        month = str(date[0])
        day = str(date[1])
        url = "http://tides.gc.ca/eng/station?type=0&date=2015%%2F%s%%2F%s&sid=%s&tz=UTC&pres=2" % (month, day, sid)
        yield scrapy.Request(url, callback=self.parse_final_level)

  # sid
  # table
  # http://tides.gc.ca/eng/station?type=0&date=2015%2F01%2F01&sid=1485&tz=UTC&pres=2
  def parse_final_level(self, response):
    sid_full = response.xpath('//div[@class="stationTextHeader"]/div/text()').extract()[0]
    p = re.compile('\(\d*\)')
    sid = re.search(p, sid_full).group(0)
    sid = sid.strip('()')
    for div in response.xpath('//div[@class="stationTextData"]/div'):
      tides_string = div.xpath('text()').extract()[0].strip()
      tides_split = tides_string.split(';')
      date = tides_split[0]
      date = date.replace('/', '')
      time = tides_split[1]
      time = time.replace(':', '')
      height_meters = tides_split[2]
      height_meters = height_meters.replace('(m)', '')
      height_feet = tides_split[3]
      height_feet = height_feet.replace('(ft)', '')
      item = TidesItem()
      item['date'] = date
      item['time'] = time
      item['height_meters'] = height_meters
      item['height_feet'] = height_feet
      item['sid'] = sid
      yield item