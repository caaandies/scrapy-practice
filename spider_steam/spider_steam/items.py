import scrapy


class SpiderSteamItem(scrapy.Item):
    name = scrapy.Field()
    categories = scrapy.Field()
    number_of_reviews = scrapy.Field()
    score = scrapy.Field()
    date = scrapy.Field()
    developer = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    platforms = scrapy.Field()

