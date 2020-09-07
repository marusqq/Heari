#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''script to scrape delfi'''

import sys,time
from bs4 import BeautifulSoup
import requests

def scrape_delfi(url):

    try:
        page = requests.get(url)

    except:     
        error_type, error_obj, error_info = sys.exc_info()      
        print('ERROR FOR URL:', url)
        print(error_type, 'Line:', error_info.tb_lineno)
        print('Error obj', error_obj)

    soup = BeautifulSoup(page.text, "html.parser") 
    
    articles = []
    article_titles = []
    article_links = []

    for article in soup.find_all('h3', class_ = "headline-title"):
        article_title = article.find('a', class_ = "CBarticleTitle")
        article_link = article.find('a')['href']
        if article_title:
            article_titles.append(article_title.text)
            article_links.append(article_link)

    articles.append(article_titles)
    articles.append(article_links)

    return articles
    #save_in_file(page.text, os.path.join('created_files/' + str(now) + '_' + url.split('.')[1] + '.txt'))