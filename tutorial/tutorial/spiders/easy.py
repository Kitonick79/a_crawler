# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tutorial.items import TutorialItem
from scrapy.loader import ItemLoader
import datetime, socket
from scrapy.loader.processors import TakeFirst

class EasySpider(CrawlSpider):
    name = 'easy'
    #allowed_domains = ['web']
    start_urls = ['https://www.avito.ru/sankt-peterburg/kvartiry/prodam?s_trg=4']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[contains(@class,"next")]')),
        Rule(LinkExtractor(restrict_xpaths='//*[@itemprop="url"]'), callback='parse_item')
        #Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        l = ItemLoader(item = TutorialItem(), response = response)
        
        l.add_xpath('price', '//*[@itemprop="price"]/@content', TakeFirst())
        l.add_xpath('rooms', '//span[contains(text(), "Количество комнат")]/parent::*/text()', re = '^[0-9]*[-]*[А-ЯЁ]?[а-яё]+[1-9]*')
        l.add_xpath('floor', '//span[contains(text(), "Этаж:")]/parent::*/text()', re= '^[0-9]*[.,]?[0-9]+')
        l.add_xpath('floors', '//span[contains(text(), "Этажей в доме:")]/parent::*/text()', re = '^[0-9]*[.,]?[0-9]+')
        l.add_xpath('Building_type', '//span[contains(text(), "Тип дома:")]/parent::*/text()', re = '[А-ЯЁ]?[а-яё]+')
        l.add_xpath('Square_m', '//span[contains(text(), "Общая площадь:")]/parent::*/text()', re = '^[0-9]*[.,]?[0-9]+')
        l.add_xpath('Kitchen_sq_m', '//span[contains(text(), "Площадь кухни:")]/parent::*/text()', re = '[0-9]*[.,]?[0-9]+')
        l.add_xpath('Square_m_living', '//span[contains(text(), "Жилая площадь:")]/parent::*/text()', re = '^[0-9]*[.,]?[0-9]+')
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()
