import scrapy

class TidesSpider(scrapy.Spider):
  name = "tides"
  allowed_domains = ["tides.gc.ca"]
  start_urls = (
    'http://tides.gc.ca/eng/',
  )

  # first level (region): select#mapSelect > option = http://tides.gc.ca/eng/find/region?id=5
  def parse(self, response):
    for region in response.xpath('//option'):
      value = region.xpath('@value').extract()[0]
      name = region.xpath('text()').extract()[0]
      url = "http://tides.gc.ca/eng/find/zone?id=%s" % value
      print value, name, url
      yield scrapy.Request(url, callback=self.parse_second_level)

  # second level (zone): select#mapSelect > option = http://tides.gc.ca/eng/find/zone?id=22
  def parse_second_level(self, response):
    for zone in response.xpath('//option'):
      value = zone.xpath('@value').extract()[0]
      name = zone.xpath('text()').extract()[0]
      url = "http://tides.gc.ca/eng/station?sid=%s" % value
      print value, name, url

# third level: select#mapSelect > option = http://tides.gc.ca/eng/station?sid=1485
# fourth level: table