#!/usr/bin/env python

'''
category_generator.py

Copyright 2017 Long Qian
Contact: lqian8@jhu.edu

This script creates categories for your Jekyll blog hosted by Github page.
No plugins required.
'''

import glob
import os
import fnmatch

post_dir = '_posts/'
category_dir = 'category/'

filenames = []
for root, dirnames, original_filenames in os.walk(post_dir):
    for filename in fnmatch.filter(original_filenames, '*.md'):
        filenames.append(os.path.join(root, filename))
    for filename in fnmatch.filter(original_filenames, '*.html'):
        filenames.append(os.path.join(root, filename))

total_categories = []
for filename in filenames:
    f = open(filename, 'r', encoding='utf8')
    crawl = False
    for line in f:
        if crawl:
            current_categories = line.strip().split()
            if current_categories[0] == 'categories:':
                total_categories.extend(current_categories[1:])
                crawl = False
                break
        if line.strip() == '---':
            if not crawl:
                crawl = True
            else:
                crawl = False
                break
    f.close()
total_categories = set(total_categories)

old_categories = glob.glob(category_dir + '*.md')
for category in old_categories:
    os.remove(category)
    
if not os.path.exists(category_dir):
    os.makedirs(category_dir)

for category in total_categories:
    category_filename = category_dir + category + '.md'
    f = open(category_filename, 'a')
    write_str = '---\nlayout: categories\ntitle: \"Category: ' + category + '\"\ncategory: ' + category + '\nrobots: noindex\n---\n'
    f.write(write_str)
    f.close()
print("Categories generated, count", total_categories.__len__())
