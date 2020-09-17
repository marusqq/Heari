#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''controller script'''

import newspaper_scrape as ns
import generate_html as html

articles = ns.scrape_newspapers()
html.generate_html(articles)