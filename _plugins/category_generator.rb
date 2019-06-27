#Category index generator
require 'yaml'

String.class_eval do
  def to_slug
    value = self.gsub(/[^\x00-\x7F]/n, '').to_s
    value.gsub!(/[']+/, '')
    value.gsub!(/\W+/, ' ')
    value.strip!
    value.downcase!
    value.gsub!(' ', '-')
    value
  end
end

def category_generator
	puts "---\nUpdating categories indexes..."
	# Get categories in current pages
	files = Dir.glob('../_posts/**/*')
	categories = {}
	files.each do |filename|
		if File.file?(filename)
			post = YAML.load_file(filename)
			unless post['categories'].nil?
				post_categories = post['categories']
				# Categories can be defined as an array or string, so we have to test how to extract them.
				if post_categories.kind_of?(Array)
					post_categories.each do |new_category|
						unless categories.include?(new_category)
							categories[new_category] = new_category.to_slug
						end
					end
				else
					unless categories.include?(post_categories)
						categories[post_categories] = post_categories.to_slug
					end
				end
			end
		end
	end
	
	puts files.length.to_s + ' posts inspected.'
	puts categories.length.to_s + ' categories found.'
	
	# Get old category pages
	old_category_files = Dir.glob('../category/**/*')
	old_categories = []
	old_category_files.each do |old_category_file|
		old_category_file['../category/'] = ''
		old_category_file['.md'] = ''
		old_categories.push(old_category_file)
	end 
	puts old_categories.length.to_s + ' old categories found'
	
	# Find any categories pages that are no longer needed, and delete them
	delete_categories = []
	old_categories.each do |old_category|
		if categories.key(old_category) == NIL
			delete_categories.push('../category/' + old_category + '.md')
		end
	end 
	delete_categories.each do |name, filename|
		unless filename.nil?
			if File.exist?(filename)
				puts 'Deleting ' + filename
				File.delete(filename)
			end
		end
	end
	#old_categories = old_categories - delete_categories	# Remove deleted categories from old categories
	
	# Find any new categories, and create pages for them
	new_categories = {}
	categories.each do |name, filename|
		unless old_categories.include?(filename)
			new_categories[name] = '../category/' + filename + '.md'
		end
	end
	new_categories.each do |name, filename|
		new_category_file = File.open(filename, 'w')
		new_category_file.puts "---\nlayout: categories\ntitle: \"Category: " + name + "\"\ncategory: " + name + "\nrobots: noindex\n---\n"
		new_category_file.close
		puts 'New file created: ' + filename
	end
	puts categories.length.to_s + " categories. (" + delete_categories.length.to_s + " removed, " + new_categories.length.to_s + " added.)\n---\n\n"
end

