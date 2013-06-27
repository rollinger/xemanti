# encoding: utf-8
require 'nokogiri'
require 'open-uri'
require 'json'

doc = Nokogiri.XML(File.open("dewiktionary_dump.xml", 'rb'))
pages = doc.xpath("//mediawiki//page")

dictionary = {}
#
# Precompile Patterns
#
re = /\[\[(.*?)\]\]/
wikilink_pattern = Regexp.new(re,Regexp::IGNORECASE)
re = /\{\{Sprache\|(.*?)\}\}/
language_pattern = Regexp.new(re,Regexp::IGNORECASE)
re = /\{\{Wortart\|(.*?)\|/
partofspeech_pattern =  Regexp.new(re,Regexp::IGNORECASE)
re = /\{\{Synonyme\}\}\n(.*?)\n/
synonyme_pattern =  Regexp.new(re,Regexp::IGNORECASE)
re = /\{\{Gegenwörter\}\}\n(.*?)\n/
antonym_pattern =  Regexp.new(re,Regexp::IGNORECASE)
re = /\{\{Oberbegriffe\}\}\n(.*?)\n/
supercategory_pattern =  Regexp.new(re,Regexp::IGNORECASE)
re = /\{\{Unterbegriffe\}\}\n(.*?)\n/
subcategory_pattern =  Regexp.new(re,Regexp::IGNORECASE)

pages.each do |page|
	word = page.at_xpath("title").inner_text
	text = page.at_css("text").inner_text
	language = text.scan(language_pattern)
	partofspeech = text.scan(partofspeech_pattern)
	synonyme = text.scan(synonyme_pattern).join(" ").scan(wikilink_pattern)
	antonyme = text.scan(antonym_pattern).join(" ").scan(wikilink_pattern)
	supercategory = text.scan(supercategory_pattern).join(" ").scan(wikilink_pattern)
	subcategory = text.scan(subcategory_pattern).join(" ").scan(wikilink_pattern)
	
	if not language.empty? and not partofspeech.empty?
		dictionary[word]= {
			"language" => language.flatten, 
			"partofspeech" => partofspeech.flatten,
			"synonyme" => synonyme.flatten,
			"antonyme" => antonyme.flatten,
			"supercategory" => supercategory.flatten,
			"subcategory" => subcategory.flatten
		} 
	end
end

File.open("wiktionary.json","w") do |f|
  f.write(dictionary.to_json)
end
