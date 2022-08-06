import scrapy

class gaiaSpider(scrapy.Spider):
    name = "gaia"

    start_urls = [
        # "https://gaiaorganics.ca/shop/"
        "https://gaiaorganics.ca/shop/page/71/"
        ]

    # either get seed names from each individual product page
    def parse(self, response):
        item_num = 1
        # all seeds (24) from one page 
        while item_num <= 25:
            print(item_num)
            for seed in response.xpath(f'/html/body/div[2]/section/div/div[1]/ul/li[{item_num}]/a'):
                
                product_page_css = seed.css('a::attr(href)') # a tags get href selected automatically

                yield from response.follow_all(product_page_css, self.product_parse)
                
            item_num += 1

        # goes to next page 
        next_arrow = response.css('.next::attr(href)')
        if next_arrow:
            yield from response.follow_all(next_arrow, self.parse)


    def product_parse(self, response):
        # gets seed name
        seed = response.css('.product_title::text').get() 

        # gets price 
        price = response.css('p.price span bdi::text').get()

        # gets seed quantity (smallest)
        seed_qty = response.css('option::text')[1].get()

        # If seed quantity is not given
        if "seeds" not in seed_qty and " g" not in seed_qty:
            seed_qty = "N/A"

        # replace unicode with ' and removes whitespace
        seed = seed.replace('\u2019', '\'').strip() 

        # remove $, CAD and whitespace
        # price = price.replace('$', '').replace('CAD', '').strip()
        
        # remove \n, ~, "seeds" and whitespace
        seed_qty = seed_qty[:11].lower().replace('seeds', '').replace('-', '').strip()

        yield {
            'seed':  seed,
            'price': price,
            'qty': seed_qty,
        }
