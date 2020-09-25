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

def split_time(time_with_date, newspaper):
    '''
    function to read different time strings from webpages
    arguments:

    time_with_date       -- string with time/date
    newspaper            -- or in other words, type of reading
    '''

    if newspaper == 'delfi':
        s_time = time_with_date.split('T')
        date = s_time[0]
        s_time = s_time[1].split('+')
        time = s_time[0]

    elif newspaper == 'lrytas':
        s_time = time_with_date.split(' ')
        date = s_time[0]
        time = s_time[1]
    
    return date, time

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

def get_new_id(articles):
    max_id = 0
    for article in articles:
        if int(article['article_no']) > max_id:
            max_id = int(article['article_no'])

    return max_id + 1 

def set_article_properties(no, newspaper, link, publish_date = None, publish_time = None, modify_date = None, modify_time = None, title = None,  photo = None, author = None, flex = None, category = None):
    '''function to set article properties

    mandatory arguments:
    no                -- article number
    newspaper         -- article newspaper name
    link              -- article link

    possible arguments:
    publish_date      -- article modify date
    publish_time      -- article publish time
    modify_date       -- article modify date
    modify_time       -- article modify time
    title             -- article title
    photo             -- article photo
    author            -- article author
    category          -- article category
    flex              -- article flex


    returns:
    articles          -- articles array with new added dict new_article
    '''

    article = {
    'article_no'                :   0,
    'article_newspaper'         :   '',
    'article_publish_date'      :   '',
    'article_publish_time'      :   '',
    'article_modify_date'       :   '',
    'article_modify_time'       :   '',
    'article_title'             :   '',
    'article_link'              :   '',
    'article_photo'             :   '',
    'article_author'            :   '',
    'article_category'          :   '',
    'article_flex'              :   ''
    }

    #mandatory
    article['article_no'] = no
    article['article_newspaper'] = newspaper
    article['article_link'] = link

    #not mandatory
    if publish_date is not None:
        article['article_publish_date'] = publish_date
    if publish_time is not None:
        article['article_publish_time'] = publish_time
    if modify_date is not None:
        article['article_modify_date'] = modify_date
    if modify_time is not None:
        article['article_modify_time'] = modify_time
    if title is not None:
        article['article_title'] = title
    if photo is not None:
        article['article_photo'] = photo
    if author is not None:
        article['article_author'] = author
    if flex is not None:
        article['article_flex'] = flex
    if category is not None:
        article['article_category'] = category
    
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
    newspaper = 'delfi'

    #loop through articles
    for article in soup.find_all("div"):
        try:
            div_class = article.get('class')
            if div_class:
                if str(div_class[0]) == 'headline':

                    #maybe it's enough
                    if article_count == 0:
                        return articles

                    link = article.find('a')['href']
                    img = article.find('img')['data-src']
                    title_html = article.find('h3')

                    #categories
                    category = ''
                    categories = link.split('/')
                    for i in range(3, len(categories) - 1):
                        if '-' in categories[i]:
                            pass
                        else:        
                            if len(category) < 1:
                                category += categories[i].capitalize()
                            else:
                                category = category + ', ' + categories[i].capitalize()

                    title = ''

                    for t in title_html.strings:
                        title += t
                    
                    #fix titles
                    title = title[:title.find('(')]
                    
                    #update article_no
                    article_no = get_new_id(articles)

                    #create new article
                    new_article = set_article_properties(
                        no = article_no, newspaper = newspaper,
                        title = title, link = link, photo = img, category = category)

                    #try to scrape other info
                    new_article = delfi_article_scrape(article = new_article)

                    #add it to articles
                    articles, article_count = add_article(articles, new_article, article_count)
           
        except:
            pass

    return articles

def delfi_article_scrape(article):
    '''
    scraping function for delfi articles

    arguments:
    article dict       -- article 

    returns:
    article dict       -- article with more properties
    
    '''
    try:
        page = requests.get(article['article_link'])

    except:
        print('Error with:', article['article_link'])
        error_type, error_obj, error_info = sys.exc_info()
        print('Exc info:', error_type, error_info, error_obj)
        print('Error line', error_info.tb_lineno)

    soup = bs(page.text, "lxml")

    '''get author name and publish time'''
    for meta in soup.find_all("meta"):
        meta_type = meta.get('name')
        if meta_type:
            if str(meta_type) == "cXenseParse:recs:author":
                article_author = meta['content']

            elif str(meta_type) == "cXenseParse:recs:publishtime":
                article_publish_date, article_publish_time = split_time(meta['content'], 'delfi')

    if article_author is not None:
        article['article_author'] = article_author
    if article_publish_date is not None:
        article['article_publish_date'] = article_publish_date
    if article_publish_time is not None:
        article['article_publish_time'] = article_publish_time

    return article

def _15min_scrape(url_to_connect, article_count, return_html = False):
    '''scraping function for 15min

    arguments:
    url_to_connect -- url of what to scrape
    article_count  -- max articles to return
    return_html    -- True if you want pure html returned (testing purposes)

    returns:
    articles       -- array of article dicts
    '''
    #connect to the page
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
    newspaper = '15min'

    #loop through articles
    for article in soup.find_all('article'):
        try:
            #maybe it's enough
            if article_count == 0:
                return articles

            title_link = article.find('a')
            link = 'https://15min.lt' + title_link['href']
            title = title_link['title']
            img = article.find('img')['data-src']
        
        except:
            print('Error with:', article)
            error_type, error_obj, error_info = sys.exc_info()
            print('Exc info:', error_type, error_info, error_obj)
            print('Error line', error_info.tb_lineno)
        
        #get safe article_no
        article_no = get_new_id(articles)
        
        #set scraped properties
        new_article = set_article_properties(no = article_no, newspaper = newspaper,
            title = title, link = link, photo = img)
        
        #try to scrape for more in article page
        new_article = _15min_article_scrape(article = new_article)

        #add new_article to articles
        articles, article_count = add_article(articles, new_article, article_count)

    return articles    

def _15min_article_scrape(article):
    '''scraping function for 15min article scrapes
    for more article properties

    arguments:
    article dict       -- article 

    returns:
    article dict       -- article with more properties
    '''

    try:
        page = requests.get(article['article_link'])

    except:
        print('Error with:', article['article_link'])
        error_type, error_obj, error_info = sys.exc_info()
        print('Exc info:', error_type, error_info, error_obj)
        print('Error line', error_info.tb_lineno)

    soup = bs(page.text, "lxml")

    '''get author name'''
    for div in soup.find_all("div"):
        div_type = div.get('class')
        if div_type:
            #print(div_type)
            if "author-info" in str(div_type):
                for authors in div.stripped_strings:
                    if authors.rstrip('\n') == 'Autorius:':
                        pass
                    else:
                        if authors is not None:
                            article['article_author'] = authors
                            break
                
    '''get date published, date modified'''
    for meta in soup.find_all("meta"):
        meta_type = meta.get('itemprop')
        if meta_type:
            if str(meta_type) == 'datePublished':
                date, time = split_time(meta['content'], 'delfi')
                if date is not None:
                    article['article_publish_date'] = date
                if time is not None:
                    article['article_publish_time'] = time

            elif str(meta_type) == 'dateModified':
                date, time = split_time(meta['content'], 'delfi')
                if date is not None:
                    article['article_modify_date'] = date
                if time is not None:
                    article['article_modify_time'] = time

    
    '''get category from article'''
    #delete what we don't consider a category

    article_split = article['article_link'].split('/')

    for need_to_delete in ('naujiena', '15min.lt', '', 'https:'):
        if need_to_delete in article_split:
            article_split.remove(need_to_delete)

    #delete the last, which is article name
    article_split.remove(article_split[len(article_split)- 1])
    category = ''
    
    for a in article_split:
        if a == 'nusikaltimaiirnelaimes':
            a = 'Nusikaltimai ir nelaimes'

        elif a.lower() == 'pasaulis-kiseneje':
            a = 'Pasaulis kiseneje'

        elif a.lower() == 'per-lietuva':
            a = 'Per Lietuva'

        if len(category) < 1:
            category = a.capitalize()
        else:
            category = category + ', ' + a.capitalize()
    
    if category is not None:
        article['article_category'] = category

    return article

def lrytas_scrape(url_to_connect, article_count, return_html = False):
    '''scraping function for lrytas

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

    soup = bs(page.text, "html.parser")

    if return_html:
        return str(soup)

    articles = []
    newspaper = 'lrytas'

    for article in soup.find_all('div'):

        # maybe its enough
        if article_count == 0:
            return articles

        
        div_class = article.get('class')
        
        if '--Articolo' in str(div_class):
            #get title and link here
            h3 = article.find_next('h3')
            title_and_link = h3.find_next('a')
            link = title_and_link['href']
            title = title_and_link.text


            #get new article id
            article_no = get_new_id(articles)

            #create new article
            new_article = set_article_properties(
                no = article_no, newspaper = newspaper, title = title,
                link = link
            )

            #try for more info
            new_article = lrytas_article_scrape(article = new_article)

            #add it to our articles
            articles, article_count = add_article(articles, new_article, article_count)


    return articles

def lrytas_article_scrape(article):
    '''scraping function for lrytas article scrapes
    for more article properties

    arguments:
    article dict       -- article 

    returns:
    article dict       -- article with more properties
    '''

    try:
        page = requests.get(article['article_link'])

    except:
        print('Error with:', article['article_link'])
        error_type, error_obj, error_info = sys.exc_info()
        print('Exc info:', error_type, error_info, error_obj)
        print('Error line', error_info.tb_lineno)

    soup = bs(page.text, "lxml")

    #look for more info
    for meta in soup.find_all('meta'):
        
        meta_property = meta.get('property')
        if meta_property:
            
            #category
            if str(meta_property) == "article:section":
                if meta['content']:
                    article['article_category'] = meta['content']

            #publish time
            elif str(meta_property) == "article:published_time":
                if meta['content']:
                    date, time = split_time(meta['content'], 'lrytas')
                    article['article_publish_date'] = date
                    article['article_publish_time'] = time

            #image
            elif str(meta_property) == "og:image":
                if meta['content']:
                    article['article_photo'] = meta['content']

    return article

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
                article_no = get_new_id(articles)

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
            article_no = get_new_id(articles)

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
articles = scrape('15min', return_html = False, last_articles=5)
#util.save_in_file(articles, '15min.html', True)
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

print_articles(articles)