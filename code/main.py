#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''main script to automate news reading'''

#workflow
    #1. scrape wanted websites from settings.json file
    #2. write them somewhere
    #3. generate a website?

import docx
from docx import Document
from docx.enum.dml import MSO_THEME_COLOR_INDEX

import json
import website_scraping.delfi as delfi
import website_scraping._15min as _15min
import website_scraping.lrytas as lrytas
import utilities as util
import os
from datetime import datetime

def to_word(text, filename):
  document = Document()
  
  for i in range(0,len(text[0])-1):
      p = document.add_paragraph(text[0][i] + ' ')
      add_hyperlink(p, text[1][i], '(link)', 'FF6347', False)

  document.save(filename)

def add_hyperlink(paragraph, url, text, color, underline):
    """
    A function that places a hyperlink within a paragraph object.

    :param paragraph: The paragraph we are adding the hyperlink to.
    :param url: A string containing the required url
    :param text: The text displayed for the url
    :return: The hyperlink object
    """

    # This gets access to the document.xml.rels file and gets a new relation id value
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    # Create the w:hyperlink tag and add needed values
    hyperlink = docx.oxml.shared.OxmlElement('w:hyperlink')
    hyperlink.set(docx.oxml.shared.qn('r:id'), r_id, )

    # Create a w:r element
    new_run = docx.oxml.shared.OxmlElement('w:r')

    # Create a new w:rPr element
    rPr = docx.oxml.shared.OxmlElement('w:rPr')

    # Add color if it is given
    if not color is None:
      c = docx.oxml.shared.OxmlElement('w:color')
      c.set(docx.oxml.shared.qn('w:val'), color)
      rPr.append(c)

    # Remove underlining if it is requested
    if not underline:
      u = docx.oxml.shared.OxmlElement('w:u')
      u.set(docx.oxml.shared.qn('w:val'), 'none')
      rPr.append(u)

    # Join all the xml elements together add add the required text to the w:r element
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)

    paragraph._p.append(hyperlink)

    return hyperlink
  
with open(os.getcwd() + '/settings.json') as f:
  data = json.load(f)

webpages_to_scrape = []
for webpage in data['webpages']:
    #get url of the websites which need scraping on settings.json
    if data['webpages'][webpage]:
        url = data['url'][webpage].rstrip('\n')
        if webpage == 'delfi':
            articles = delfi.scrape_delfi(url)
            data['articles'] = articles

            try:
              os.remove('created_files/articles_delfi.txt')
            except:
              print('no created_files/articles_delfi.txt')

            try:
              os.remove('created_files/articles_delfi.docx')
            except:
              print('no created_files/articles_delfi.docx')

            util.save_in_file(articles, 'created_files/articles_delfi.txt')
            to_word(articles, 'created_files/articles_delfi.docx')

        elif webpage == '15min':
            articles = _15min.scrape_15min(url)
            data['articles'] = articles

            try:
              os.remove('created_files/articles_15min.txt')
            except:
              print('no created_files/articles_15min.txt')

            try:
              os.remove('created_files/articles_15min.docx')
            except:
              print('no created_files/articles_15min.docx')

            util.save_in_file(articles, 'created_files/articles_15min.txt')
            to_word(articles, 'created_files/articles_15min.docx')
        
        elif webpage == 'lrytas':
            articles = lrytas.scrape_lrytas(url)
            data['articles'] = articles

            try:
              os.remove('created_files/articles_lrytas.txt')
            except:
              print('no created_files/articles_lrytas.txt')

            try:
              os.remove('created_files/articles_lrytas.docx')
            except:
              print('no created_files/articles_lrytas.docx')

            util.save_in_file(articles, 'created_files/articles_lrytas.txt', False)
            to_word(articles, 'created_files/articles_lrytas.docx')
# #       
