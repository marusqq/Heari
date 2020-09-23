#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''script for utilities'''

import json
import os

import docx
from docx import Document

def save_in_file(text_to_save, filename, testing = False):
    o = open(filename, 'w+', encoding='utf-8')
    if testing:
        o.write(text_to_save)
        return
        
    for i in range(0, len(text_to_save[0]) - 1):
        o.write(text_to_save[0][i] + '\n')
        o.write(text_to_save[1][i] + '\n')
        o.write('\n')
    o.close()
    return

def read_json(filename = 'settings.json'):
    with open(os.getcwd() + '/' + filename) as f:
        data = json.load(f)
    
    return data

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