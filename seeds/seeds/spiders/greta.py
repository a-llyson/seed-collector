import scrapy

class gretaSpider(scrapy.Spider):
    name = "greta"
    
    start_urls = ["https://www.seeds-organic.com/collections/all"]

    # either get seed names from each individual product page
    def parse(self, response):
        item_num = 1

        # all seeds (24) from one page 
        while item_num <= 24:
            for seed in response.xpath(f'/html/body/main/div[2]/div/div[2]/div/ul/li[{item_num}]/div/div/div[2]/div[1]/h3/a'):
                
                product_page_css = seed.css('a::attr(href)') # a tags get href selected automatically

                yield from response.follow_all(product_page_css, self.product_parse)
                
            item_num += 1
        
        # goes to next page 
        next_arrow = response.css('.pagination__item--prev::attr(href)')
        if next_arrow:
            yield from response.follow_all(next_arrow, self.parse)


    def product_parse(self, response):
        # gets seed name
        seed = response.css('h1.product__title::text').get() 

        # gets price 
        price = response.css('span.price-item--regular::text').get()

        # gets seed quantity (the first label)
        seed_qty = response.css('#template--15861094482164__main-1-0').xpath('@value').get()

        # If seed quantity is not given
        if "seeds" not in seed_qty and " g" not in seed_qty:
            seed_qty = "N/A"

        # replace unicode with ' and removes "organic" and whitespace
        seed = seed.replace('\u2019', '\'').replace('- Organic', '').replace('-Organic', '').strip() 

        # remove $, CAD and whitespace
        price = price.replace('$', '').replace('CAD', '').strip()
        
        # remove ~, "seeds" and whitespace
        seed_qty = seed_qty.replace('~', '').replace('seeds', '').strip()

        yield {
            'seed':  seed,
            'price': price,
            'qty': seed_qty,
            'store': 'greta'
        }
