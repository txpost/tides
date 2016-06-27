import scrapy

from tides.items import TidesItem

class TidesSpider(scrapy.Spider):
  name = "tides"
  allowed_domains = ["tides.gc.ca"]
  start_urls = [
    # 'http://tides.gc.ca/eng/'
    'http://tides.gc.ca/eng/station?sid=1485'
  ]

  def parse(self, response):
    for table in response.xpath('//div[@class="grid-12 indent-medium"]/div/table'):
      date = table.xpath('@title').extract()[0][-10:]
      date = date.replace('-', '')
      for row in table.xpath('.//tbody/tr'):
        time = row.xpath('td/text()').extract()[0]
        height_meters = row.xpath('td/text()').extract()[1]
        height_feet = row.xpath('td/text()').extract()[2]
        tide = 1
        if float(height_meters) < 1:
          tide = 0
        item = TidesItem()
        item['date'] = date
        item['time'] = time
        item['height_meters'] = height_meters
        item['height_feet'] = height_feet
        item['tide'] = tide
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