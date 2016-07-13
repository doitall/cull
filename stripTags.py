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
from collections import defaultdict
mat = defaultdict(dict)
filtered_words = []

r = '\"+|\.+|/+|,+| +|\t+|\r+|\n+'


stop_words = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
#    def handle_starttag(self, tag, attrs):
#        x=1
#    def handle_endtag(self, tag):
#	x=1

    def handle_data(self, data):
 	 oldline = ""
         val=0
         global filtered_words
        
	 filtered_string = filter(lambda x: x in string.printable, data)


         words = re.split(r, filtered_string)
         for word in words:
           	if len(word) > 0 and word.lower() not in stop_words:
			#print word.lower()
           		filtered_words.append(word.lower())


def stripHTML(text):

 global filtered_words
 filtered_words = []
 if len(text) == 0:
   return ""
 if text == " ":
   return ""

 if len(text.replace(' \n','')) == 0:
   return ""

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
 return filtered_words

def stripEmail(text):
  wordlist = []
  import email
  msg = email.message_from_string(text)  

  if msg.is_multipart():
    for part in msg.walk():
        ctype = part.get_content_type()
        cdispo = str(part.get('Content-Disposition'))

        # skip any text/plain (txt) attachments
        if (ctype == 'text/plain' or ctype == 'text/html') and 'attachment' not in cdispo:
            wordlist = wordlist + stripHTML(part.get_payload(decode=True))  # decode
# not multipart - i.e. plain text, no attachments, keeping fingers crossed
  else:
     wordlist = stripHTML(msg.get_payload(decode=True))

  if __name__ == "__main__":
 	print wordlist
  return wordlist
'''
  if msg.is_multipart():
	for payload in msg.get_payload():
          if type(payload.get_payload()) is not str:
	   for payload1 in payload.get_payload():
             if type(payload1.get_payload()) is not str:
              print type(payload1.get_payload())
	      for payload2 in payload1.get_payload():
	       print "!======"+payload2.get_payload()+"++++++++++++"
               stripTags(payload2.get_payload())
             else:
	      print "======"+payload1.get_payload()+"++++++++++++"
              stripTags(payload1.get_payload())
          else:
	     print "$====="+payload.get_payload()+"++++++++++++$"
             stripTags(payload.get_payload())
  else:
   	stripTags(msg.get_payload())
'''
#  text = filter(lambda x: x in string.printable, text)
# parser = MyHTMLParser() 
#  parser.feed(text)


if __name__ == "__main__":
 fname, file_extension = os.path.splitext(sys.argv[1])
 if '.html' in file_extension or '.htm' in file_extension:
  with open (sys.argv[1], "r") as myfile:
        stripHTML(myfile.read())
 else: #assume email format
  with open (sys.argv[1], "r") as myfile:
	stripEmail(myfile.read())
