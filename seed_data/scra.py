import scrapy

# command line: scrapy runspider scra.py -o airfares.json

class FareSpider(scrapy.Spider):
    name = "fares"
    start_urls = open('seed_data/test.txt')

# make a file with all the URLs to extract data from (start_urls)

    def parse(self, response):
        destination = response.css('h1.ttl').extract()
        fare = response.css('div.div7').extract()



        """ SAMPLE CODE BELOW:
        for fare in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
            }

        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        """