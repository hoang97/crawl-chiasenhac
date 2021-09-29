# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# from scrapy.loader.processors import TakeFirst
from itemloaders.processors import TakeFirst


class ChiasenhacItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    file_name = scrapy.Field(
        out_processor = TakeFirst()
    )
    folder_name = scrapy.Field(
        out_processor = TakeFirst()
    )
    file_urls = scrapy.Field()
    files = scrapy.Field()
