#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''script to scrape 15min'''

import sys,time
from bs4 import BeautifulSoup
import requests

def scrape_15min(url):

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

    for article in soup.find_all('h4', class_ = "vl-title"):
        
        article_text = str(article.text).replace("\n", "")
        article_link = article.find('a')['href']

        article_titles.append(article_text)
        article_links.append('https://15min.lt' + article_link)
        

    articles.append(article_titles)
    articles.append(article_links)

    return articles