import scrapy

class gaiaSpider(scrapy.Spider):
    name = "gaia"

    start_urls = ["https://gaiaorganics.ca/shop/"]

    # either get seed names from each individual product page
    def parse(self, response):
        item_num = 1
        # all seeds (24) from one page 
        while item_num <= 25: 
            xpath = f'/html/body/div[2]/section/div/div[1]/ul/li[{item_num}]/a'
            if not (response.xpath(xpath)):
                xpath = f'/html/body/div[1]/section/div/div[1]/ul/li[{item_num}]/a'

            seed=response.xpath(xpath)[0]

            product_page_css = seed.css('a::attr(href)') # a tags get href selected automatically

            yield from response.follow_all(product_page_css, self.product_parse)
                
            item_num += 1


        # scrapy throws error for page 72 but everything on page 72 is processed
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
        if response.css('option::text'):
            seed_qty = response.css('option::text')[1].get()
        else:
            seed_qty = "OOS"

        # If seed quantity is not given
        if "seeds" not in seed_qty and " g" not in seed_qty and "OOS" not in seed_qty:
            seed_qty = "N/A"

        # replace unicode with ' and removes whitespace
        seed = seed.replace('\u2019', '\'').strip() 

        # remove $, CAD and whitespace
        # price = price.replace('$', '').replace('CAD', '').strip()
        
        # remove \n, ~, $, "seeds" and whitespace
        seed_qty = seed_qty[:11].lower().replace('seeds', '').replace('-', '').replace('$', '').strip()

        # to filter out the live plants for pickup at their ottawa location

        if price:
            yield {
                'seed':  seed,
                'price': price,
                'qty': seed_qty,
            }
