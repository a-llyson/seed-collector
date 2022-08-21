import scrapy
import re as regex

# infinite scroll site
class heritageSpider(scrapy.Spider):
    name = "heritage"

    page_num = 1
    heritage_url = "https://heritageharvestseed.com/collections/all?page={}"
    start_urls = [heritage_url.format(page_num)]

    # either get seed names from each individual product page
    def parse(self, response):
        item_num = 1

        while item_num <= 12: 
            seed = response.xpath(f'/html/body/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/div[{item_num}]/div/div[2]/h5/a')

            product_page_css = seed.css('a::attr(href)') # a tags get href selected automatically

            yield from response.follow_all(product_page_css, self.product_parse)
                
            item_num += 1
        
        # all products on scroll down page
        # goes to next page
        page_num = int(regex.findall("\d+", response.request.url)[0]) + 1
        if page_num <= 75:
            yield scrapy.Request(url=self.heritage_url.format(page_num), callback=self.parse)


    def product_parse(self, response):
        # gets seed name
        seed = response.css('h1::text').get() 

        # gets price 
        price = response.css('span.money::text').get()

        # gets seed quantity in sentence with regex (\d+ means any number 1+ times, 
        # \D+ means not a digit 1+ times so it will only match "seed quantity" + 
        # "seed name" (maybe) + "seeds" 
        # and not "80 days from transplant There are 25 Ancho Poblano Pepper Seeds")
        if response.css('p').re("\d+\D+seeds per packet"):
            seed_qty = response.css('p').re("\d+\D+seeds per packet")[0]
        elif response.css('p').re("\d+\D+seeds"):
            seed_qty = response.css('p').re("\d+\D+seeds")[0]
        elif response.css('select.single-option-selector').re("\d+\D+seeds"): 
            # if it has dropdown
            seed_qty = response.css('select.single-option-selector').re("\d+\D+seeds")[0]
            seed_qty = regex.findall("\d+", seed_qty)[0]   
        else:
            # Not listed
            seed_qty = "N/A"
        

        # gets seed name and adds back ' and removes whitespace
        seed = seed.rsplit('-', 1)[0].replace('\u2019', '\'').replace('\u2018', '\'').strip()

        # remove $, CAD and whitespace
        price = price.replace('$', '').strip()
        
        # remove \n, ~, "seeds" and whitespace
        seed_qty = regex.sub('\D', '', seed_qty)
        # seed_qty = seed_qty.replace('~', '').replace('seeds', '').strip()

        yield {
            'seed':  seed,
            'price': price,
            'qty': seed_qty,
            'store': 'heritage harvest seeds'
        }
