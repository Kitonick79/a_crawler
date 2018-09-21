import scrapy
from tutorial.items import TutorialItem
from scrapy.loader import ItemLoader
import datetime, socket
from scrapy.loader.processors import TakeFirst

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    # def __init__(self, *args, **kwargs): 
    #   super(QuotesSpider, self).__init__(*args, **kwargs) 
    #   self.urls = [kwargs.get('urls')]


    def start_requests(self):
        urls = [
            'https://www.avito.ru/sankt-peterburg/kvartiry/studiya_30.2_m_1019_et._1370247928?back=%2Fsankt-peterburg%2Fkvartiry%2Fprodam%3Fp%3D1%23i1370247928'
            #'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        l = ItemLoader(item = TutorialItem(), response = response)
        
        l.add_xpath('price', '//*[@itemprop="price"]/@content', TakeFirst())
        l.add_xpath('rooms', '//span[contains(text(), "Количество комнат")]/parent::*/text()', re = '[А-ЯЁ]?[а-яё]+[1-9]*')
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