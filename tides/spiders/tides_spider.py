import scrapy

from tides.items import TidesItem

class TidesSpider(scrapy.Spider):
  name = "tides"
  allowed_domains = ["tides.gc.ca"]
  start_urls = [
    # 'http://tides.gc.ca/eng/'
    # 'http://tides.gc.ca/eng/station?sid=1485'
    'http://tides.gc.ca/eng/station?type=0&date=2016%2F01%2F01&sid=6457&tz=UTC&pres=2'
  ]

  def parse(self, response):
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
      yield item
  
  # region
  # select#mapSelect > option 
  # http://tides.gc.ca/eng/find/region?id=5
  # def parse(self, response):
  #   for region in response.xpath('//option'):
  #     value = region.xpath('@value').extract()[0]
  #     name = region.xpath('text()').extract()[0]
  #     url = "http://tides.gc.ca/eng/find/zone?id=%s" % value
  #     print value, name, url
  #     yield scrapy.Request(url, callback=self.parse_second_level)

  # zone 
  # select#mapSelect > option 
  # http://tides.gc.ca/eng/find/zone?id=22
  # def parse_second_level(self, response):
  #   for zone in response.xpath('//option'):
  #     value = zone.xpath('@value').extract()[0]
  #     name = zone.xpath('text()').extract()[0]
  #     url = "http://tides.gc.ca/eng/station?sid=%s" % value
  #     print value, name, url
  #     yield scrapy.Request(url, callback=self.parse_final_level)

  # sid
  # table
  # http://tides.gc.ca/eng/station?sid=1485
  # def parse_final_level(self, response):
  #   for station in response.xpath('//table'):
  #     title = station.
  #     print station