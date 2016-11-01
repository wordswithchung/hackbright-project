import scrapy

# command line: scrapy runspider scra.py -o test.json

class FareSpider(scrapy.Spider):
    name = "fares"
    # make a file with all the URLs to extract data from (start_urls)
    start_urls = ['http://www.faredetective.com/farehistory/flights-from-Zurich-ZRH-to-Toronto-YYZ.html']

    def parse(self, response):
        
        # Title area with from and to airport codes. Sample data:
        # '<h1 class="ttl ttl_ft">Airfare History Charts - Zurich (ZRH) 
        # to Toronto (YYZ)</h1>'

        header = response.css('h1.ttl').extract_first()
        lst = header.split()

        def extract(string, start='(', stop=')'):
            """Got the function from here: http://bit.ly/2e6ZqM2"""
            return string[string.index(start)+1:string.index(stop)]

        for item in lst:
            if "(" in item:
                extract(item)
        
        # Fare area with price and cheapest month info. Sample data: u'<div 
        # class="div7">From:Zurich<br>To:Toronto<br>Lowest price found:771.5
        # <br>Average price: 1063<br>Cheapest months to travel: November<br>
        # </div>'

        fare = response.css('div.div7').extract_first()
        fare = fare.encode('ascii', 'ignore').split("<br>")
        yield {
            'from': fare[0],
            'to': fare[1],
            'lowest_price': fare[2],
            'average_price': fare[3],
            'cheapest_month': fare[4],
            }