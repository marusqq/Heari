#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''controller script'''

import scrape as sc
import generate_html as html

articles = sc.scrape_main()
html.generate_html(articles)