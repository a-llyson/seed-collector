import scrapy
import re as regex

class hawthornSpider(scrapy.Spider):
    name = "hawthorn"

    start_urls = [
        "https://hawthornfarm.ca/pages/vegetables",
        "https://hawthornfarm.ca/collections/herbs",
        "https://hawthornfarm.ca/collections/flowers",
    ]

    # either get seed names from each individual product page
    def parse(self, response):

        # for vegetable page
        for seed in response.css("a.featured-box"):
            seed = seed.css("a::attr(href)")
            yield from response.follow_all(seed, self.parse)

        # for flowers and herbs and individual vegetables
        for item in response.css("a.product-grid-item"):
            item = item.css("a::attr(href)")
            yield from response.follow_all(item, self.product_parse)


    def product_parse(self, response):
        # gets seed name
        seed = response.css('h1::text').get() 

        # gets price 
        price = response.css('span.h1 span::text').get()

        # gets seed quantity in sentence with regex
        if response.css('option').re("\d+\D+seed"):
            seed_qty = response.css('option').re("\d+\D+seed")[0]
        elif response.css('option').re("\d+\D+day"):
            # for a typo on their site
            seed_qty = response.css('option').re("\d+\D+day")[0] 
        else:
            seed_qty = "N/A"

        # gets seed name and adds back ' and removes whitespace
        seed = seed.replace('\u2019', '\'').replace('\u2018', '\'').strip()

        # remove $ and whitespace
        price = price.replace('$', '').strip()
        
        # removes non digits
        seed_qty = regex.sub('\D', '', seed_qty)
        if seed_qty == "":
            seed_qty = "N/A"
        # seed_qty = seed_qty.replace('~', '').replace('seeds', '').strip()

        yield {
            'seed':  seed,
            'price': price,
            'qty': seed_qty,
            'store': 'hawthorn',
            'url': response.request.url,
        }
