#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''main script to automate news reading'''

#workflow
    #1. scrape wanted websites from settings.json file
    #2. write them somewhere
    #3. generate a website?

import website_scraping.delfi as delfi
import website_scraping._15min as _15min
import website_scraping.lrytas as lrytas
import website_scraping.verslozinios as verslozinios

import utilities as util
import os
from datetime import datetime

def get_settings():
  return util.read_json()

def scrape_newspapers():
  
    data = get_settings()
    articles = data['webpages']

    for webpage in data['webpages']:
      #get url of the websites which need scraping on settings.json
        if data['webpages'][webpage]:
            url = data['url'][webpage].rstrip('\n')

            if webpage == 'delfi':
                articles = delfi.scrape_delfi(url)
                data['articles'][webpage] = articles
                
            elif webpage == '15min':
                articles = _15min.scrape_15min(url)
                data['articles'][webpage] = articles

            elif webpage == 'lrytas':
                articles = lrytas.scrape_lrytas(url)
                data['articles'][webpage] = articles

            elif webpage == 'verslozinios':
                articles = verslozinios.scrape_vzinios(url)
                data['articles'][webpage] = articles

            try:
                os.remove('created_files/articles_' + webpage + '.txt')
            except:
                print('no created_files/articles_' + webpage + '.txt')

            try:
                os.remove('created_files/articles_' + webpage + '.docx')
            except:
                print('no created_files/articles_' + webpage + '.docx')

            util.save_in_file(articles, 'created_files/articles_' + webpage + '.txt', True)
            util.to_word(articles, 'created_files/articles_' + webpage + '.docx')
    
    return data

# scrape_newspapers()
# generate_html()