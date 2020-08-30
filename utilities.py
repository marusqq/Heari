#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''script for utilities'''

def save_in_file(text_to_save, filename, testing = False):
    o = open(filename, 'w+', encoding='utf-8')
    if testing:
        o.write(text_to_save)
        return
    #for text in text_to_save:
    for i in range(0, len(text_to_save[0]) - 1):
        o.write(text_to_save[0][i] + '\n')
        o.write(text_to_save[1][i] + '\n')
        o.write('\n')
    o.close()
    return