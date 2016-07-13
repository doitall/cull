# Usage: stripTags <file_name.html>
# Output: One text word per line 

import re
import os
import sys
import string
import re
from HTMLParser import HTMLParser
import lxml
from lxml.html.clean import Cleaner

r = '\"+|\.+|/+|,+| +|\t+|\r+|\n+'


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
#    def handle_starttag(self, tag, attrs):
#        x=1
#    def handle_endtag(self, tag):
#	x=1

    def handle_data(self, data):
	 filtered_string = filter(lambda x: x in string.printable, data)
         words = re.split(r, filtered_string)
         for word in words:
           if len(word) > 0:
           	print word.lower()


def stripTags(text):
 cleaner = Cleaner()
 cleaner.javascript = True # This is True because we want to activate the javascript filter
 cleaner.style = True      # This is True because we want to activate the styles & stylesheet filter
 text = lxml.html.tostring(cleaner.clean_html(lxml.html.parse(text)))
 text = filter(lambda x: x in string.printable, text)
 parser = MyHTMLParser() 
 parser.feed(text)

 return text


#main
with open (sys.argv[1], "r") as myfile:
        stripTags(myfile)
