import scrapy

class gretaSpider(scrapy.Spider):
    name = "greta"
    start_urls = ["https://www.seeds-organic.com/collections/all"]

    # either get seed names from /all page or from each individual product page?
    def parse(self, response):
        item_num = 1
        while item_num <= 24:
            for seed_name in response.xpath(f'/html/body/main/div[2]/div/div[2]/div/ul/li[{item_num}]/div/div/div[2]/div[1]/h3/a'):
                
                # seed = seed_name.css('::text').get() # returns '\n        seed_name\n      '
                # seed = seed.replace('\n', '') # strips \n from name, could also strip -organic if wanted)
                # seed = seed.replace('\u2019', '\'') # replace unicode with right single quotation mark
                # seed = seed.strip() # strips whitespace
                
                product_page_css = seed_name.css('a::attr(href)') # a tags get href selected automatically

                yield from response.follow_all(product_page_css, self.product_parse)
                
                # or if new page is loaded, then set it back to 0
                if item_num > 24:
                    break
                else:
                    item_num += 1

    def product_parse(self, response):
        for block in response.xpath('//*[@id="ProductInfo-template--15861094482164__main"]'):
            # gets title
            seed = block.css('h1.product__title::text').get() 

            # gets price 
            price = block.css('span.price-item--regular::text').get()

            # gets seed quantity (the first label)
            seed_qty = block.css('label::text').get()

            # If not seed quantity is not given
            if "seeds" not in seed_qty:
                seed_qty = "N/A"

            # replace unicode with ' and removes "organic" and whitespace
            seed = seed.replace('\u2019', '\'').replace('- Organic', '').strip() 

            # remove $, CAD and whitespace
            price = price.replace('$', '').replace('CAD', '').strip()
            
            # remove \n, ~, "seeds" and whitespace
            seed_qty = seed_qty.replace('\n', '').replace('~', '').replace('seeds', '').strip()

            yield {
                'seed':  seed,
                'price': price,
                'qty': seed_qty,
            }
