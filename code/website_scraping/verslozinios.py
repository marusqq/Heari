#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''script to scrape lrytas'''

import sys, time
from bs4 import BeautifulSoup
import requests

def scrape_vzinios(url):

    try:
        page = requests.get(url)

    except:     
        error_type, error_obj, error_info = sys.exc_info()      
        print('ERROR FOR URL:', url)
        print(error_type, 'Line:', error_info.tb_lineno)
        print('Error obj', error_obj)

    soup = BeautifulSoup(page.text, "html.parser") 
    
    #return HTML
    #return str(soup)
    
    articles = []
    article_titles = []
    article_links = []

    for article in soup.find_all('div', class_ = "one-article"):
        article_text = article.find('a')['title']
        article_link = article.find('a')['href']
            
        article_titles.append(article_text)
        article_links.append(article_link)
        
    articles.append(article_titles)
    articles.append(article_links)

    return articles