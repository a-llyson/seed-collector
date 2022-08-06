import scrapy

class gretaSpider(scrapy.Spider):
    name = "greta"
    start_urls = ["https://www.seeds-organic.com/collections/all"]

    # either get seed names from /all page or from each individual product page?
    def parse(self, response):
        item_num = 1
        print("ere")
        for seed_name in response.xpath(f'/html/body/main/div[2]/div/div[2]/div/ul/li[{item_num}]/div/div/div[2]/div[1]/h3/a'):
            
            seed = seed_name.css('::text').get() # returns '\n        seed_name\n      '
            seed = seed.replace('\n', '') # strips \n from name, could also strip -organic if wanted)
            seed = seed.strip() # strips whitespace

            yield {
                'seed':  seed
            }

            # product_page_css = seed_name.css('') # a tags get href selected automatically
            # yield from response.follow_all(product_page_css, self.productParse)
            
            # or if new page is loaded, then set it back to 0
            if item_num > 24:
                item_num = 1
            else:
                item_num += 1

    def productParse(self, response):
        print("hello")
    
