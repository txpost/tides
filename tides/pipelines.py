# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class TidesPipeline(object):
  def __init__(self):
    self.csvwriter = csv.writer(open('items.csv', 'wb'))

  def process_item(self, item, tides_spider):
    row = [item['sid'], item['date'], item['time'], item['height_meters'], item['height_feet']]
    self.csvwriter.writerow(row)
    return item