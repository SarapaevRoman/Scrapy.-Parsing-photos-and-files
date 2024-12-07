import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.loader import ItemLoader
from ..items import UnsplashItem
from itemloaders.processors import MapCompose


class UnsplashcomSpider(CrawlSpider):
    name = "unsplashcom"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/t/deck-the-halls"]

    rules = (Rule(LinkExtractor(restrict_xpaths='//div[@class="jWMSo"]'), callback="parse_item", follow=True),
             Rule(LinkExtractor(restrict_xpaths='//a[@class="wuIW2 R6ToQ"]'),))

    def parse_item(self, response):
                   
        loader = ItemLoader(item=UnsplashItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)
        #Автор
        loader.add_xpath('author', '//a[@class="vGXaw uoMSP kXLw7 R6ToQ JVs7s R6ToQ"]/text()')

        #Категория
        categories = response.xpath('//a[@class="ZTh7D kXLw7"]/text()').get()
        loader.add_value('categories', categories if categories else 'unknown')

        #Описание
        loader.add_xpath('description', '//h1[@class="vev3s"]/text()')


        #Cсылки
        relativ_image_url = response.xpath('//div[@class="hSqFa sINnN"]/button/div/img[@srcset]/@src').get()
        
        loader.add_value('image_urls', relativ_image_url)

        yield loader.load_item()

        
