#Tag index generator
require 'yaml'
def tag_generator
	puts "---\nUpdating tags indexes..."
	# Get tags in current pages
	files = Dir.glob('../_posts/**/*')
	tags = []
	files.each do |filename|
		if File.file?(filename)
			post = YAML.load_file(filename)
			unless post['tags'].nil?
				# Tags can be defined as an array or string, so we have to test how to extract them.
				if post['tags'].kind_of?(Array)
					post_tags = post['tags']
				else
					post_tags = post['tags'].split(' ')
				end
				post_tags.each do |new_tag|
					unless tags.include?(new_tag)
						tags.push(new_tag)
					end
				end
			end
		end
	end
	puts files.length.to_s + ' posts inspected.'
	puts tags.length.to_s + ' tags found.'
	
	# Get old tag pages
	old_tag_files = Dir.glob('../tag/**/*')
	old_tags = []
	old_tag_files.each do |old_tag_file|
		old_tag_file['../tag/'] = ''
		old_tag_file['.md'] = ''
		old_tags.push(old_tag_file)
	end 
	puts old_tags.length.to_s + ' old tags found'
	
	# Find any tags pages that are no longer needed, and delete them
	delete_tags = {}
	old_tags.each do |old_tag|
		unless tags.include?(old_tag)
			delete_tags[old_tag]= '../tag/' + old_tag + '.md'
		end
	end 
	delete_tags.each do |name, filename|
		if File.exist?(filename)
			puts 'Deleting ' + filename
			File.delete(filename)
		end
	end
	#old_tags = old_tags - delete_tags	# Remove deleted tags from old tags
	
	# Find any new tags, and create pages for them
	new_tags = {}
	tags.each do |tag|
		unless old_tags.include?(tag)
			new_tags[tag] = '../tag/' + tag + '.md'
		end
	end
	new_tags.each do |name, filename|
		new_tag_file = File.open(filename, 'w')
		new_tag_file.puts "---\nlayout: tags\ntitle: \"Tag: " + name + "\"\ntag: " + name + "\nrobots: noindex\n---\n"
		new_tag_file.close
		puts 'New file created: ' + filename
	end
	puts tags.length.to_s + " tags. (" + delete_tags.length.to_s + " removed, " + new_tags.length.to_s + " added.)\n---\n\n"
end