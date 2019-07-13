#!/bin/bash
cd "../../_plugins/"
ruby cat_tag_generator.rb
cd ".."
bundle exec jekyll build
