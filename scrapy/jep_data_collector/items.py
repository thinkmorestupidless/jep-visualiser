# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JepItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    full_jep_link = scrapy.Field()
    owner = scrapy.Field()
    type = scrapy.Field()
    scope = scrapy.Field()
    status = scrapy.Field()
    release = scrapy.Field()
    component = scrapy.Field()
    discussion = scrapy.Field()
    effort = scrapy.Field()
    duration = scrapy.Field()
    reviewed_by = scrapy.Field()
    endorsed_by = scrapy.Field()
    created = scrapy.Field()
    updated = scrapy.Field()
    issue = scrapy.Field()

class JdkItem(scrapy.Item):
    version = scrapy.Field()
    release_date = scrapy.Field()
    summary = scrapy.Field()
    jeps = scrapy.Field()
