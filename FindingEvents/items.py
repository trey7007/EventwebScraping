# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class FindingEventsItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

def datetimesplitter(datetime):
    return datetime.replace("-" , "@")

class EventItem(scrapy.Item):
    event = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    datetime = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    # To call a preprocessing function (listed above).
    # date = scrapy.Field(serializer = datetimesplitter)
    genre = scrapy.Field()
    