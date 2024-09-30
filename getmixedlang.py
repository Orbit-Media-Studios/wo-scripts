# Libraries
import regex
import re
import string
import requests
import lxml
from bs4 import BeautifulSoup
from lingua import Language, LanguageDetectorBuilder

# Get data: https://www.topcoder.com/thrive/articles/web-crawler-in-python
url = "https://www.orbitmedia.com/"
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
f = requests.get(url, headers = headers)
linkslist = []
soup = BeautifulSoup(f.content, 'lxml')

# Get all links (to loop this in a crawl)
print("\nGet all links from " + url + " for crawling:\n")
links = soup.find_all('a', href=True)
num = 0
for atag in links:
  print("url: " + atag['href'])

# Function to remove tags: https://www.geeksforgeeks.org/remove-all-style-scripts-and-html-tags-using-beautifulsoup/
def remove_tags(html):
 
    # End tags like sentences
    html = html.replace("<", ".<")

    # parse html content
    soup = BeautifulSoup(html, "html.parser")
 
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
 
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)
 
# Case insensitive replace
def ireplace(old, repl, text):
    return re.sub('(?i)'+re.escape(old), lambda m: repl, text)
# Text cleanup

# Return cleaned text
print("\nJust the text from " + url + ":\n")
cleantext = remove_tags(str(soup))
cleantext = re.sub('[^0-9a-zA-Z.]+', ' ', cleantext)
cleantext = cleantext.replace(" .", "") # extra dots
cleantext = cleantext.replace("|", "\n")
cleantext = cleantext.replace("-", "\n")
ireplace("LinkedIn", "", cleantext) # case insensitive find/replace
ireplace("Youtube", "", cleantext) # case insensitive find/replace
ireplace("Facebook", "", cleantext) # case insensitive find/replace
ireplace("Twitter", "", cleantext) # case insensitive find/replace
ireplace("Edit Post", "", cleantext) # case insensitive find/replace
ireplace("SaaS", "", cleantext) # case insensitive find/replace
cleantext = cleantext.replace("  ", " ") # double space
print(cleantext)

# Detect the languages: https://pypi.org/project/lingua-language-detector/ -- degree of confidence
print("\nDetected languages at " + url + ":\n")
languages = [Language.ENGLISH, Language.FRENCH,Language.CHINESE,Language.JAPANESE]
detector = LanguageDetectorBuilder.from_languages(*languages).build()
confidence_values = detector.compute_language_confidence_values(cleantext)
for language, value in confidence_values:
  print(f"{language.name}: {value:.2f}")

# Raw language values
print("\nBreakdown of languages at " + url + ":\n")
detector = LanguageDetectorBuilder.from_languages(*languages).build()
for result in detector.detect_multiple_languages_of(cleantext):
  print(f"{result.language.name}: '{cleantext[result.start_index:result.end_index]}'")