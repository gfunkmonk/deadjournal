cd "../../_plugins/"
ruby cat_tag_generator.rb
cd ".."
bundle exec jekyll serve -I --config _config.yml,_config.dev.yml