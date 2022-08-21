#!/bin/bash

. ./venv/Scripts/activate

cd seeds
scrapy crawl greta
# scrapy crawl gaia
# scrapy crawl hawthorn
# scrapy crawl heritage
# scrapy crawl osc
