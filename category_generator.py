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
import os.path
import fnmatch
import string

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

if not os.path.exists(category_dir):
    os.makedirs(category_dir)

old_categories = []
new_catgory_slugs = []
for category in total_categories:
    new_catgory_slugs.append(slugify(category).lower())

old_category_files = glob.glob(category_dir + '*.md')
for category in old_category_files:
    old_category = category.replace('category\\','').replace('.md','')
    if old_category not in new_catgory_slugs:
        print(old_category)
        old_categories.append(old_category)
for category in old_categories:
    old_category_file = 'category\\' + category + '.md'
    print('Removing old category page: ' + old_category_file)
    os.remove(old_category_file)

for category in total_categories:
    category_filename = category_dir + slugify(category).lower() + '.md'
    if not os.path.exists(category_filename):
        print('New category page generated:',category_filename)
        f = open(category_filename, 'a')
        write_str = '---\nlayout: categories\ntitle: \"Category: ' + category + '\"\ncategory: ' + category + '\nrobots: noindex\n---\n'
        f.write(write_str)
        f.close()
print("Categories count: ", total_categories.__len__())
