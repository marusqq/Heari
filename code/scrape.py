#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''controller script for scraping websites'''

import json, requests, sys
import utilities as util
from bs4 import BeautifulSoup as bs


def scrape(newspaper, last_articles = 20, return_html = False):
    '''scraping controller

    arguments:
    newspaper           -- name of the newspaper
    last_articles       -- last x articles to return
    return_html         -- True if you need pure html

    returns:
    articles[dicts]     -- array of article dicts
    '''
    data = util.read_json()

    if data['webpages'][newspaper]:

        url = data['url'][newspaper]

        if newspaper == 'delfi':
            return delfi_scrape(url_to_connect = url, article_count = last_articles, return_html = return_html)

        elif newspaper == '15min':
            return _15min_scrape(url_to_connect = url, article_count = last_articles, return_html = return_html)

        elif newspaper == 'lrytas':
            return lrytas_scrape(url_to_connect = url, article_count = last_articles, return_html = return_html)

        elif newspaper == 'verslozinios':
            return verslozinios_scrape(url_to_connect = url, article_count = last_articles, return_html = return_html)

        #TODO alfa retarded html scraping
        elif newspaper == 'alfa':
            return alfa_scrape(url_to_connect = url, article_count = last_articles, return_html = return_html)

        elif newspaper == 'bernardinai':
            return bernardinai_scrape(url_to_connect = url, article_count = last_articles, return_html = return_html)

        # elif newspaper == 'lrt-lt':
        #     return lrt-lt_scrape(url_to_connect = url, article_count = last_articles, return_html = return_html)
        
        # elif newspaper == 'tv3-lt':
        #     return tv3-lt_scrape(url_to_connect = url, article_count = last_articles, return_html = return_html)

        # elif newspaper == 'respublika':
        #     return respublika_scrape(url_to_connect = url, article_count = last_articles, return_html = return_html)

        # elif newspaper == 'valstietis':
        #     return valstietis_scrape(url_to_connect = url, article_count = last_articles, return_html = return_html)

        # elif newspaper == 'vakaruekspresas':
        #     return vakaruekspresas_scrape(url_to_connect = url, article_count = last_articles, return_html = return_html)

        # elif newspaper == 'diena':
        #     return diena_scrape(url_to_connect = url, article_count = last_articles, return_html = return_html)

        else:
            print('Newspaper with name', newspaper, "can't be scraped")
            return [' ', ' ', ' ']

def print_articles(articles):
    for article in articles:
        for key, value in article.items():
            print(key, ':', value)
        print('-----')

def add_article(articles, new_article, article_count):
    '''function to add new article

    arguments:
    articles          -- articles dict
    new_article       -- new_article_dict
    article_count     -- article_count to article_info

    returns:
    articles          -- articles array with new added dict new_article
    article_count     -- returns article_count + 1
    '''

    #add new_article to articles
    articles.append(new_article)
    
    # remove one to article count
    article_count -= 1

    return articles, article_count

def set_article_properties(no, newspaper, date = None, time = None, title = None, link = None, photo = None, author = None, flex = None):
    '''function to set article properties

    mandatory arguments:
    no                -- article number
    newspaper         -- article newspaper name

    possible arguments:
    date              -- article date
    time              -- article time
    title             -- article title
    link              -- article link
    photo             -- article photo
    author            -- article author
    flex              -- article flex

    returns:
    articles          -- articles array with new added dict new_article
    '''

    article = {
    'article_no'        :   0,
    'article_newspaper' :   '',
    'article_date'      :   '',
    'article_time'      :   '',
    'article_title'     :   '',
    'article_link'      :   '',
    'article_photo'     :   '',
    'article_author'    :   '',
    'article_flex'      :   ''
    }   

    article['article_no'] = no
    article['article_newspaper'] = newspaper
    if date is not None:
        article['article_date'] = date
    if time is not None:
        article['article_time'] = time
    if title is not None:
        article['article_title'] = title
    if link is not None:
        article['article_link'] = link
    if photo is not None:
        article['article_photo'] = photo
    if author is not None:
        article['article_author'] = author
    if flex is not None:
        article['article_flex'] = flex

    return article

def delfi_scrape(url_to_connect, article_count, return_html = False):
    '''scraping function for delfi

    arguments:
    url_to_connect -- url of what to scrape
    article_count  -- max articles to return
    return_html    -- True if you want pure html returned (testing purposes)

    returns:
    articles       -- array of article dicts
    '''
    
    #try to connect
    try:
        page = requests.get(url_to_connect)

    except:
        print('Error with:', url_to_connect)
        error_type, error_obj, error_info = sys.exc_info()
        print('Exc info:', error_type, error_info, error_obj)
        print('Error line', error_info.tb_lineno)

    soup = bs(page.text, "lxml")

    if return_html:
        return str(soup)

    articles = []
    article_no = 0
    newspaper = 'delfi'

    #loop through articles
    for article in soup.find_all("div"):
        try:
            div_class = article.get('class')
            if div_class:
                if str(div_class[0]) == 'headline':
                    link = article.find('a')['href']
                    img = article.find('img')['data-src']
                    title_html = article.find('h3')
                    title = ''

                    for t in title_html.strings:
                        title += t
                    
                    #fix titles
                    title = title[:title.find('(')]
                    
                    #update article_no
                    article_no += 1

                    #create new article
                    new_article = set_article_properties(
                        no = article_no, newspaper = newspaper,
                        title = title, link = link, photo = img)

                    #add it to articles
                    articles, articles_count = add_article(articles, new_article, article_count)
        
                    
        except:
            continue

    print_articles(articles)
    quit()

    return articles

def _15min_scrape(url_to_connect, article_count, return_html = False):
    '''scraping function for 15min

    arguments:
    url_to_connect -- url of what to scrape
    article_count  -- max articles to return
    return_html    -- True if you want pure html returned (testing purposes)

    returns:
    articles       -- array of article dicts
    '''
    
    try:
        page = requests.get(url_to_connect)

    except:
        print('Error with:', url_to_connect)
        error_type, error_obj, error_info = sys.exc_info()
        print('Exc info:', error_type, error_info, error_obj)
        print('Error line', error_info.tb_lineno)

    soup = bs(page.text, "lxml")

    if return_html:
        return str(soup)

    articles = []
    article_titles = []
    article_links = []
    article_photos = []

    for article in soup.find_all('h4', class_ = "vl-title"):
        
        article_text = str(article.text).replace("\n", "")
        article_link = article.find('a')['href']

        article_titles.append(article_text)
        article_links.append('https://15min.lt' + article_link)
        article_photos.append('photo')

    articles.append(article_titles)
    articles.append(article_links)
    articles.append(article_photos)

    return articles    

def lrytas_scrape(url_to_connect, article_count, return_html = False):
    '''scraping function for lrytas

    arguments:
    url_to_connect -- url of what to scrape
    article_count  -- max articles to return
    return_html    -- True if you want pure html returned (testing purposes)

    returns:
    articles[][]   -- article_text, article_link, article_photo
    '''
    
    try:
        page = requests.get(url_to_connect)

    except:
        print('Error with:', url_to_connect)
        error_type, error_obj, error_info = sys.exc_info()
        print('Exc info:', error_type, error_info, error_obj)
        print('Error line', error_info.tb_lineno)

    soup = bs(page.text, "html.parser")

    if return_html:
        return str(soup)

    articles = []
    article_titles = []
    article_links = []
    article_photos = []

    for article in soup.find_all('h3'):
        
        article_text = article.text.split('\n')
        if len(article_text) > 1:
            article_text = article_text[1]
            article_link = article.find('a')

            if article_link is not None:
                article_link = article.find('a')['href']

        else:
            continue
            
        article_titles.append(article_text)
        article_links.append(article_link)
        article_photos.append('photo')

    articles.append(article_titles)
    articles.append(article_links)
    articles.append(article_photos)

    return articles

def verslozinios_scrape(url_to_connect, article_count, return_html = False):
    '''scraping function for verslozinios

    arguments:
    url_to_connect -- url of what to scrape
    article_count  -- max articles to return
    return_html    -- True if you want pure html returned (testing purposes)

    returns:
    articles[][]   -- article_text, article_link, article_photo
    '''
    
    try:
        page = requests.get(url_to_connect)

    except:
        print('Error with:', url_to_connect)
        error_type, error_obj, error_info = sys.exc_info()
        print('Exc info:', error_type, error_info, error_obj)
        print('Error line', error_info.tb_lineno)

    soup = bs(page.text, "html.parser")

    if return_html:
        return str(soup)

    articles = []
    article_titles = []
    article_links = []
    article_photos = []

    for article in soup.find_all('div', class_ = "one-article"):
        article_text = article.find('a')['title']
        article_link = article.find('a')['href']
            
        article_titles.append(article_text)
        article_links.append(article_link)
        article_photos.append('photo')

    articles.append(article_titles)
    articles.append(article_links)
    articles.append(article_photos)

    return articles

def alfa_scrape(url_to_connect, article_count, return_html = False):
    '''scraping function for alfa
    
    arguments:
    url_to_connect -- url of what to scrape
    article_count  -- max articles to return
    return_html    -- True if you want pure html returned (testing purposes)

    returns:
    articles       -- array of article dicts
    '''
    #connection to the page
    try:
        page = requests.get(url_to_connect)

    except:
        print('Error with:', url_to_connect)
        error_type, error_obj, error_info = sys.exc_info()
        print('Exc info:', error_type, error_info, error_obj)
        print('Error line', error_info.tb_lineno)

    soup = bs(page.text, "html.parser")

    if return_html:
        return str(soup)

    articles = []
    article_titles = []
    article_links = []
    article_photos = []
    
    #im not sure how to make this work
    return None
    
    
    for article in soup.find_all('script'):
        try:
            if (article['type'] is not None) and article['type'] == 'text/javascript':
                print(type(article))
                print(article)
                print(article)
        except:
            print('Error with:', url_to_connect)
            error_type, error_obj, error_info = sys.exc_info()
            print('Exc info:', error_type, error_info, error_obj)
            print('Error line', error_info.tb_lineno)
            pass   
           
        #print(article['src'])
        input()
        # article_text = article.find('a')['title']
        # article_link = article.find('a')['href']
            
        # article_titles.append(article_text)
        # article_links.append(article_link)
        # article_photos.append('photo')

    articles.append(article_titles)
    articles.append(article_links)
    articles.append(article_photos)

    #return 'articles'
    return articles

def bernardinai_scrape(url_to_connect, article_count, return_html = False):
    '''scraping function for bernardinai

    arguments:
    url_to_connect -- url of what to scrape
    article_count  -- max articles to return
    return_html    -- True if you want pure html returned (testing purposes)

    returns:
    articles       -- array of article dicts
    '''

    #try to connect
    try:
        page = requests.get(url_to_connect)

    except:
        print('Error with:', url_to_connect)
        error_type, error_obj, error_info = sys.exc_info()
        print('Exc info:', error_type, error_info, error_obj)
        print('Error line', error_info.tb_lineno)

    soup = bs(page.text, "lxml")

    if return_html: 
        return str(soup)

    articles = []
    article_no = 0
    newspaper = 'bernardinai'

    #get two headers
    for article in soup.find_all('p'):

        #check - maybe it's enough
        if article_count == 0:
            return articles
        
        p_class = article.get('class')
        if p_class:
            if "header-quote" in p_class:
                
                #scrape the properties
                title_first = article.find('span').text
                title_second = article.find('a')
                link = title_second['href']
                title_first = title_first[:-1] + ': '
                title = title_first + title_second.text
                
                #update article_no
                article_no += 1

                #set scraped properties
                new_article = set_article_properties(no = article_no, newspaper = newspaper,
                    title = title, link = link)
                
                #add new_article to articles
                articles, article_count = add_article(articles, new_article, article_count)

    #loop through articles
    for article in soup.find_all('article'):
        try:
            authors = []
            for author in article.find_all("p"):
                p_class = author.get('class')
                if "author" in str(p_class):
                    authors.append(author.text)
            title = article.find('h3')
            link = title.parent
            long_title = title.find_next('p')
            img = article.find('img')

            #add up long and short titles
            _title = title.text[:-1] + '. ' + long_title.text

            #fix up other properties of articles
            _link = link['href']
            _img = img['src']
            _author = ', '.join(authors)
            
            #update article_no
            article_no += 1

            #create a new article
            new_article = set_article_properties(
            no = article_no, newspaper = newspaper, 
            title = _title, link = _link, photo = _img, author = _author)
    
            #add it to articles
            articles, article_count = add_article(articles, new_article, article_count)
        
        except:
            continue
        
    print_articles(articles)
    
    return articles

# scrape('delfi')
print(scrape('delfi'), return_html = False)
# scrape('15min')
# scrape('lrytas')
# scrape('verslozinios')
# #not finished
# scrape('alfa')
# util.save_in_file(scrape('bernardinai', return_html = False), 
                        #'bernardinai_pure_html.txt', 
                        #False)

# scrape('lrt-lt')
# scrape('tv3-lt')
# scrape('respublika')
# scrape('valstietis')
# scrape('vakaruekspresas')
# scrape('diena')