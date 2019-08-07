# Regenerate tags & categories, then run full build.

cd "../../_plugins/"
ruby cat_tag_generator.rb
cd ".."
bundle exec jekyll build
cd .\scripts\windows\
