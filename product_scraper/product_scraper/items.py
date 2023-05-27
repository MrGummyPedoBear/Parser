# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    publisher = scrapy.Field()
    authors = scrapy.Field()
    journal = scrapy.Field()
    affiliation = scrapy.Field()
    pissn = scrapy.Field()
    eissn = scrapy.Field()
    doi = scrapy.Field()
    year = scrapy.Field()
    volume = scrapy.Field()
    issue = scrapy.Field()
    pages = scrapy.Field()
    abstract = scrapy.Field()
    references = scrapy.Field()