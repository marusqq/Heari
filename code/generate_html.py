#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''script for html generating'''

def generate_html(articles):
    _print_articles(articles)
    return

def _print_articles(articles):
    for article in articles:
        for key, value in article.items():
            print(key, ':', value)
        print('-----')
