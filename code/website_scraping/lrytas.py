#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''script to scrape lrytas'''

import sys,time
from bs4 import BeautifulSoup
import requests

def scrape_lrytas(url):

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

    for article in soup.find_all('h3'):
        # print(article)
        # articles.append(article)
        
        article_text = article.text.split('\n')
        if len(article_text) > 1:
            article_text = article_text[1]

            article_link = article.find('a')
            if article_link is not None:
                article_link = article.find('a')['href']
        else:
            continue
            
        print(article_text)
        print(article_link)
        input()
        article_titles.append(article_text)
        article_links.append(article_link)
        
    
        # if article_text and article.find('a'):
        #     article_link = article.find('a')['href']
        #     article_titles.append(article_text)
        #     article_links.append(article_link)
    #return page.text
    articles.append(article_titles)
    articles.append(article_links)

    return articles