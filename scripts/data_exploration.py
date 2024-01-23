import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pdfplumber
import time
import pandas as pd

# set data path
raw_path = '../data/raw_data/'
proc_path = '../data/processed_data/'

# set URLs
book_microEcon = 'https://assets.openstax.org/oscms-prodcms/media/documents/Microeconomics3e-WEB.pdf?_gl=1*1klko0h*_ga*MTI0MDU1MDk4OC4xNzA1OTY4NjQ0*_ga_T746F8B0QC*MTcwNTk2ODY0My4xLjEuMTcwNTk2ODgzMC40MC4wLjA.'

# PDFs
# microEcon
req_bMicroEcon = requests.get(book_microEcon)

# write to file
with open(raw_path + 'book_microEcon.pdf', 'wb') as f_out:
    f_out.write(req_bMicroEcon.content)

# create a container pandas
microEcon_df = pd.DataFrame(columns = ['content'])

# parse using pdfplumber
with pdfplumber.open(raw_path + 'book_microEcon.pdf') as pdf_in:
    # get pages to iterate over it
    pages = pdf_in.pages

    for i, p in enumerate(pages):
        microEcon_df.loc[i, 'content'] = p.extract_text()

    microEcon_df.to_csv(proc_path + 'book_microEcon.csv')

# HTML
cnbc_url = 'https://www.cnbc.com/economy/'

# webdriver
wd = webdriver.Firefox()

# load page
wd.get(cnbc_url)

# wait 15 seconds
time.sleep(15)

# get raw HTML
cnbc_html = wd.page_source

# soup it
cnbc_soup = BeautifulSoup(cnbc_html, 'html.parser')

# output it
with open(raw_path + 'raw_cnbc.html', 'w', encoding = 'utf-8') as f_out:
    f_out.write(cnbc_soup.prettify())

with open(raw_path + 'raw_cnbc.html', 'r', encoding = 'utf-8') as f_in:
    cnbc_soup = BeautifulSoup(f_in.read(), 'html.parser')

# container pandas dataframe
cnbc_df = pd.DataFrame(columns = ['href', 'headline'])

# find headlines and save to pdf
card_titles = cnbc_soup.find_all('a', class_ = 'Card-title')

i = 0
# store card titles
for ct in card_titles:

    # get link and headline
    href = ct['href'].strip()
    headline = ct.text.strip()

    cnbc_df.loc[i] = (href, headline)

    # get latest_i of dataframe
    i = cnbc_df.shape[0]

cnbc_df.to_csv(proc_path + 'cnbc.csv')

