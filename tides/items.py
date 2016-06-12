# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TidesItem(scrapy.Item):
  date = scrapy.Field()
  time = scrapy.Field()
  heightM = scrapy.Field()
  heightFt = scrapy.Field()
  site = scrapy.Field()
  sid = scrapy.Field()
  tz = scrapy.Field()
  tide = scrapy.Field()