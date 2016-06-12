import scrapy

class TidesSpider(scrapy.Spider):
  name = "tides"
  allowed_domains = ["http://tides.gc.ca/eng"]
  start_urls = (
    'http://tides.gc.ca/eng/',
  )

  def parse(self, response):
    for region in response.xpath('//option'):
      value = region.xpath('@value').extract()
      name = region.xpath('text()').extract()
      print value, name

# first level (region): select#mapSelect > option = http://tides.gc.ca/eng/find/region?id=5
# second level (zone): select#mapSelect > option = http://tides.gc.ca/eng/find/zone?id=22
# third level: select#mapSelect > option = http://tides.gc.ca/eng/station?sid=1485
# fourth level: table