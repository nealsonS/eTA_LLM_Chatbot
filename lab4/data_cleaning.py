import re

CLEANR = re.compile('<.*?>')
#CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext


########## or

from bs4 import BeautifulSoup
cleantext = BeautifulSoup(raw_html, "lxml").text
