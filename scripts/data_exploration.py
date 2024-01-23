import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pdfplumber
import time
import pandas as pd
import csv
import os

# set data path
raw_path = '../data/raw_data/'
proc_path = '../data/processed_data/'

# set URLs
book_microEcon = 'https://assets.openstax.org/oscms-prodcms/media/documents/Microeconomics3e-WEB.pdf?_gl=1*1klko0h*_ga*MTI0MDU1MDk4OC4xNzA1OTY4NjQ0*_ga_T746F8B0QC*MTcwNTk2ODY0My4xLjEuMTcwNTk2ODgzMC40MC4wLjA.'
book_math = 'https://web.math.ucsb.edu/~agboola/teaching/2021/winter/122A/rudin.pdf'

# PDFs
# microEcon
req_bMicroEcon = requests.get(book_microEcon)
req_bMath = requests.get(book_math)

# write to file
with open(raw_path + 'book_microEcon.pdf', 'wb') as f_out:
    f_out.write(req_bMicroEcon.content)
with open(raw_path + 'book_math.pdf', 'wb') as f_out1:
    f_out1.write(req_bMath.content)


# create a container pandas
microEcon_df = pd.DataFrame(columns = ['content'])
math_df = pd.DataFrame(columns = ['content'])

# parse using pdfplumber
with pdfplumber.open(raw_path + 'book_microEcon.pdf') as pdf_in:
    # get pages to iterate over it
    pages = pdf_in.pages

    for i, p in enumerate(pages):
        microEcon_df.loc[i, 'content'] = p.extract_text()

    microEcon_df.to_csv(proc_path + 'book_microEcon.csv')

with pdfplumber.open(raw_path + 'book_math.pdf') as pdf_in:
    # get pages to iterate over it
    pages = pdf_in.pages

    for i, p in enumerate(pages):
        math_df.loc[i, 'content'] = p.extract_text()

    math_df.to_csv(proc_path + 'book_math.csv')

# HTML
cnbc_url = 'https://www.cnbc.com/economy/'

# webdriver
wd = webdriver.Firefox()

# load page
wd.get(cnbc_url)

# wait 15 seconds
time.sleep(5)

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



# URL for Wired's mathematics section
wired_math_url = 'https://www.wired.com/tag/mathematics/'

# Requesting the webpage
response_wired_math = requests.get(wired_math_url)

# Parsing the HTML of the page
soup_wired_math = BeautifulSoup(response_wired_math.content, 'html.parser')

# Locating the section with summaries
summary_items_wired_math = soup_wired_math.find_all('div', class_='summary-list__items')

# Collecting titles and links
titles_links_wired = []
for summary_item in summary_items_wired_math:
    article_links = summary_item.find_all('a', class_='SummaryItemHedLink-civMjp')
    for article_link in article_links:
        title_wired = article_link.find('h3', class_='SummaryItemHedBase-hiFYpQ').get_text(strip=True)
        full_link_wired = 'https://www.wired.com' + article_link['href']
        titles_links_wired.append((title_wired, full_link_wired))

# Path for saving the CSV file
csv_filename_wired = 'wired_mathematics_titles.csv'
full_csv_path_wired = os.path.join(proc_path, csv_filename_wired)


# Writing data to CSV
with open(full_csv_path_wired, 'w', newline='', encoding='utf-8') as csv_file_wired:
    csv_writer_wired = csv.writer(csv_file_wired)
    csv_writer_wired.writerow(['Title', 'Link'])  # Header row
    csv_writer_wired.writerows(titles_links_wired)

print(f'Data saved to {full_csv_path_wired}')


