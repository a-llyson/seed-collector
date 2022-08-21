import scrapy
import re as regex

class oscSpider(scrapy.Spider):
    name = "osc"

    start_urls = [
        "https://www.oscseeds.com/product-category/vegetables/",
        "https://www.oscseeds.com/product-category/herbs/",
        "https://www.oscseeds.com/product-category/seed-starting-supplies/",
        "https://www.oscseeds.com/product-category/gardening-accessories/",
        "https://www.oscseeds.com/?s=Flower&post_type=product",
        "https://www.oscseeds.com/product-category/lawn-seed-ground-covers-and-alternatives/",
        "https://www.oscseeds.com/product-category/collections/",
        "https://www.oscseeds.com/product-category/legumes-and-forage-crops/",
        "https://www.oscseeds.com/product-category/trees-and-ornamental-grasses/",
    ]

    # either get seed names from each individual product page
    def parse(self, response):

        # for circle product pages
        for seed in response.css("li.product-category"):
            
            seed = seed.css('a::attr(href)')
            print(seed.get())
            yield from response.follow_all(seed, self.square_parse)

        

    def square_parse(self, response):

        # for purely item product pages (squares)
        for item in response.css("h3.product-title"):
            item = item.css("a::attr(href)")
            print(item.get())
            yield from response.follow_all(item, self.product_parse)

        # all products on scroll down page
        # goes to next page
        # response.css("a.next::attr('href')").get()
        next_arrow = response.css('.next::attr(href)')
        if next_arrow:
            yield from response.follow_all(next_arrow, self.square_parse)

    def product_parse(self, response):
        # gets seed name
        seed = response.css('h1::text').get() 

        # gets price 
        price = response.css('span.woocommerce-Price-amount bdi::text').get()

        # gets seed quantity in sentence with regex (\d+ means any number 1+ times, 
        # \D+ means not a digit 1+ times so it will only match "seed quantity" + 
        # "seeds/pkt"
        seed_qty = response.css('p').re("\d+\D+seeds/pkt")
        if seed_qty:
            seed_qty = seed_qty[0]
        elif response.css('p').re("\d+\D+seed"):
            seed_qty = response.css('p').re("\d+\D+seed")[0]
        else:
            seed_qty = "N/A"

        # gets seed name and adds back ' and removes whitespace
        seed = seed.replace('\u2019', '\'').replace('\u2018', '\'').strip()

        # remove $, CAD and whitespace
        price = price.replace('$', '').strip()
        
        # remove \n, ~, "seeds" and whitespace
        seed_qty = regex.sub('\D', '', seed_qty)
        if seed_qty == "":
            seed_qty = "N/A"
        # seed_qty = seed_qty.replace('~', '').replace('seeds', '').strip()

        yield {
            'seed':  seed,
            'price': price,
            'qty': seed_qty,
            'store': 'ontario seed company',
            'url': response.request.url,
        }
