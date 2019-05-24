#!/usr/bin/env python

'''
category_generator.py

Copyright 2017 Long Qian
Contact: lqian8@jhu.edu

This script creates categories for your Jekyll blog hosted by Github page.
No plugins required.
'''

import re
import glob
import os
import fnmatch

post_dir = '_posts/'
category_dir = 'category/'


def slugify(s):
    """
    Simplifies ugly strings into something URL-friendly.
    >>> print slugify("[Some] _ Article's Title--")
    some-articles-title
    """

    # "[Some] _ Article's Title--"
    # "[some] _ article's title--"
    s = s.lower()

    # "[some] _ article's_title--"
    # "[some]___article's_title__"
    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')

    # "[some]___article's_title__"
    # "some___articles_title__"
    s = re.sub('\W', '', s)

    # "some___articles_title__"
    # "some   articles title  "
    s = s.replace('_', ' ')

    # "some   articles title  "
    # "some articles title "
    s = re.sub('\s+', ' ', s)

    # "some articles title "
    # "some articles title"
    s = s.strip()

    # "some articles title"
    # "some-articles-title"
    s = s.replace(' ', '-')

    return s


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
            params = line.strip().split(':')
            if params[0] == 'categories':
                current_categories = params[1].strip().split(',')
                current_categories = [cat.replace('[', '').replace(']', '').replace('"', '') for cat in current_categories]
                total_categories.extend(current_categories)
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
print('Categories', total_categories)

old_categories = glob.glob(category_dir + '*.md')
for category in old_categories:
    os.remove(category)
    
if not os.path.exists(category_dir):
    os.makedirs(category_dir)

for category in total_categories:
    category_filename = category_dir + slugify(category) + '.md'
    print('category_filename',category_filename)
    f = open(category_filename, 'a')
    write_str = '---\nlayout: categories\ntitle: \"Category: ' + category + '\"\ncategory: ' + category + '\nrobots: noindex\n---\n'
    f.write(write_str)
    f.close()
print("Categories generated, count", total_categories.__len__())
