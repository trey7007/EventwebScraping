import scrapy
from scrapy import Request
from FindingEvents.items import EventItem
from scrapy.exceptions import CloseSpider


class BandsspiderSpider(scrapy.Spider):

    name = "bandsspider"
    allowed_domains = ["bandsintown.com"]
    #this is the Madison city ID
    start_urls = ["https://www.bandsintown.com/?city_id=5261457"]

    # custom_settings = {
    #     'FEEDS': {
    #         'banddata.json' : {'format': 'json', 'overwrite': True}
    #     }
    # }
   

    def __init__(self):
        pass    
    #     self.results = []
    #     self.name = "bandpider1111"


    def parse(self, response):
        genres = response.css('a.Ch7k1T1DAWrArEous5hi ::attr(href)').getall()

        for genre in genres:
            yield Request(response.urljoin(genre), self.parse_genre)

        
    def parse_genre(self, response):
        disallowed_genre = ["All Genres" , "Christian/Gospel", "Country", "Classical"]

        bands = response.css('div.AtIvjk2YjzXSULT1cmVx')
        genre = response.css('a.DEtdg_ebWp1WssEkz7Dh')
        g = genre.css('span._xT1T7soLIel8_WGwaWX::text').get()

        if g in disallowed_genre:
            pass
        else:
            for band in bands:
                details_page_url = band.css('a.HsqHp2xM2FkfSdjy1mlU ::attr(href)').get()
            
                band_deets = {
                    'genre' : genre.css('span._xT1T7soLIel8_WGwaWX::text').get(),
                    'name' : band.css('div._5CQoAbgUFZI3p33kRVk::text').get(),
                    'location' : band.css('div.bqB5zhZmpkzqQcKohzfB::text').get(),
                    'date' : band.xpath('//div[@class="r593Wuo4miYix9siDdTP"]/div/text()').get(),
                }

                yield response.follow(details_page_url, callback=self.parse_details_page, cb_kwargs=band_deets)

    
    def parse_details_page(self, response, genre, name, location, date ):

        band_item = EventItem()

        band_item['event'] = "Concert"
        band_item['city'] = response.xpath('//div[@class="e6YFaVBz8eqoPeVSqavc"]/div/div/a/text()').get(),
        band_item['name'] = name,
        band_item['location'] = location,
        band_item['datetime'] = date,
        band_item['genre'] = genre,
        band_item['date'] = response.css('h2.EfW1v6YNlQnbyB7fUHmR::text').get()
        
        yield band_item

    @classmethod
    def handle_spider_error(cls, failure):
        if failure.check(CloseSpider):
            cls.logger.error("\n\n\n\n Spider closed: %s", failure.value)

        ### To continue between pages
        # next_page = response.css('li.next a ::attr(href)').get()
        # if next_page is not None:
        #     if 'catalogue/' in next_page:
        #         next_page_url = 'https://books.toscrape.com/' + next_page
        #     else:
        #         next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
        #     yield response.follow(next_page_url, callback=self.parse)
            
