# Usage: stripTags <file_name.html>
# Usage: stripTags <file_name> 
# Second usage treated as email file with possible embedded html 
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
 	 oldline = ""
         val=0
        
	 filtered_string = filter(lambda x: x in string.printable, data)


         words = re.split(r, filtered_string)
         for word in words:
           	if len(word) > 0:
           		print word.lower()


def stripTags(text):
 cleaner = Cleaner()
 cleaner.javascript = True # This is True because we want to activate the javascript filter
 cleaner.style = True      # This is True because we want to activate the styles & stylesheet filter
 text = lxml.html.tostring(cleaner.clean_html(lxml.html.fromstring(text)))
 text = filter(lambda x: x in string.printable, text)
 entities = [
          ('nbsp;', ''),
          ('&#13;', ''),
          ('202=;', ''),
         ]

 for before, after in entities:
    text = text.replace(before, after)
 oldline=""
 for line in text.splitlines():
	if line.endswith('='):
		nline = line[:-1]
		oldline += nline
		continue
	oldline += line	

 parser = MyHTMLParser() 
 parser.feed(oldline)

 return text

def stripEmail(text):
  import email
  msg = email.message_from_string(text)  
  if msg.is_multipart():
	for payload in msg.get_payload():
            stripTags(payload.get_payload())
  else:
   	stripTags(msg.get_payload())
#  text = filter(lambda x: x in string.printable, text)
# parser = MyHTMLParser() 
#  parser.feed(text)


#main
fname, file_extension = os.path.splitext(sys.argv[1])
if '.html' in file_extension or '.htm' in file_extension:
 with open (sys.argv[1], "r") as myfile:
        stripTags(myfile.read())
else: #assume email format
 with open (sys.argv[1], "r") as myfile:
	stripEmail(myfile.read())
