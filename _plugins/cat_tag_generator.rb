require_relative 'category_generator'
require_relative 'tag_generator'
category_generator
tag_generator
	
#Jekyll::Hooks.register :site, :pre_render do |site|
#	STDOUT.write 'Genrating category and tag indexes'
#	category_generator
#	tag_generator
#end
