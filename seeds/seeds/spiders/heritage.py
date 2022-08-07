import scrapy
import re as regex

# infinite scroll site
class heritageSpider(scrapy.Spider):
    name = "heritage"
    
    start_urls = ["https://heritageharvestseed.com/collections/all"]

    # either get seed names from each individual product page
    def parse(self, response):
        item_num = 1

        while True:
            seed = response.xpath(f'/html/body/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/div[{item_num}]/div/div[2]/h5/a')

            if not seed:
                break

            product_page_css = seed.css('a::attr(href)') # a tags get href selected automatically

            yield from response.follow_all(product_page_css, self.product_parse)
                
            item_num += 1
        
        # all products on scroll down page
        # goes to next page 
        # next_arrow = response.css('.pagination__item--prev::attr(href)')
        # if next_arrow:
        #     yield from response.follow_all(next_arrow, self.parse)


    def product_parse(self, response):
        # gets seed name
        seed = response.css('h1::text').get() 

        # gets price 
        price = response.css('span.money::text').get()

        # gets seed quantity in sentence with regex
        seed_qty = response.css('p').re("\d+\D+seeds per pack")[0]
        seed_qty = regex.findall("\d+", seed_qty)[0]


        # gets seed name and discards scientific name and removes whitespace
        seed = seed.split('-', 1)[0].strip()

        # remove $, CAD and whitespace
        price = price.replace('$', '').strip()
        
        # remove \n, ~, "seeds" and whitespace
        # seed_qty = seed_qty.replace('~', '').replace('seeds', '').strip()

        yield {
            'seed':  seed,
            'price': price,
            'qty': seed_qty,
        }
