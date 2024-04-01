import requests
from bs4 import BeautifulSoup
import re

def remove_html_tags(text):
    pattern = re.compile('<.*?>')
    return re.sub(pattern, '', text)

def get_soup(URL):
	return BeautifulSoup(requests.get(URL).text, 'html.parser')

def get_p_to_str(soup):
	return [(remove_html_tags(p.get_text())) for p in main_soup.find_all('p')]

if __name__ == '__main__':

	URL = 'https://en.wikipedia.org/wiki/Clinical_pharmacology'
	main_soup = get_soup(URL)
	
	# find branches
	main_p = get_p_to_str(main_soup)
	print(f'Scraping {URL}')

	# branch links
	branch_links = []

	branch_soup = main_soup.find('div', class_ = 'mw-content-ltr mw-parser-output').find('ul')

	print('Getting sublinks')
	for li in branch_soup.find_all('li'):

		for a in li.find_all('a', href=True):
			suburl = a.get('href')
			branch_url = f'https://en.wikipedia.org/{suburl}'
			branch_links.append(branch_url)

	branch_p = []
	done_links = [] # to keep track of links scraped
	for link in branch_links:

		if '#cite_note' not in link:
			if link not in done_links:
				print(f'Scraping: {link}')

				b_soup = get_soup(link)
				b_p = get_p_to_str(b_soup)
				branch_p.extend(b_p)

				done_links.append(link)

	main_p.extend(branch_p)

	OUT_PATH = 'wikip.txt'
	print(f'Outputting to {OUT_PATH}')

	with open(OUT_PATH, 'w') as f_out:
		f_out.writelines(main_p)

