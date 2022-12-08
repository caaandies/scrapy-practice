import scrapy
from urllib.parse import urlencode
from urllib.parse import urljoin
from ..items import SpiderSteamItem


queries = ['shooters', 'racing', '2D']


class SteamspiderSpider(scrapy.Spider):
    name = 'SteamSpider'

    def start_requests(self):
        for query in queries:
            url = 'https://store.steampowered.com/search/?' + urlencode({'term' : query, 'page': '1'})
            yield scrapy.Request(url=url, callback=self.parse_response)
            url = 'https://store.steampowered.com/search/?' + urlencode({'term' : query, 'page': '2'})
            yield scrapy.Request(url=url, callback=self.parse_response)



    def parse_response(self, response):
        for game in response.xpath("//a[contains(@href,'app')]/@href"):
            game0 = response.urljoin(game.extract())
            yield scrapy.Request(url=game0, callback=self.parse_game_page)


    def parse_game_page(self, response):
        if response.xpath('//*[@class="not_yet"]').extract(): #еще не выпущена
            return
        items = SpiderSteamItem()
        name = response.xpath('//*[@id="appHubAppName_responsive"]/text()').extract()
        categories = response.xpath('//div[@class="blockbg"]/a[@href]/text()').extract()
        number = response.xpath('//meta[@itemprop="reviewCount"]/@content').extract()
        score = response.xpath('//div[@itemprop="aggregateRating"]//span[@itemprop="description"]/text()').extract()
        date = response.xpath('//div[@class="date"]/text()').extract()
        developer = response.xpath('//div[@id="developers_list"]/a/text()').extract()
        tags = response.xpath('//*[@id="genresAndManufacturer"]/span/a/text()').extract()
        price = response.xpath('//div[@class="game_purchase_price price" or @class="discount_final_price"]/text()').extract()
        platforms = response.xpath('//div[contains(@class, "sysreq_tab")]/@data-os').extract()
        items['name'] = ''.join(name).strip()
        items['categories'] = '/'.join(map(lambda x: x.strip(), categories[1:])).strip()
        items['number_of_reviews'] = ''.join(number).strip()
        items['score'] = ''.join(score).strip()
        items['date'] = ''.join(date).strip()
        items['developer'] = ''.join(developer).strip()
        items['tags'] = '/'.join(map(lambda x: x.strip(), tags)).strip()
        items['price'] = price[0].strip()
        items['platforms'] = '/'.join(map(lambda x: x.strip(), platforms)).strip()
        yield items
