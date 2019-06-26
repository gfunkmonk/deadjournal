cd "_plugins/"
ruby cat_tag_generator.rb
cd ".."
bundle exec jekyll serve --config _config.yml,_config.dev.yml