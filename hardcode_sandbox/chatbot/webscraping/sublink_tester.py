from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':

	'''URL = 'https://biology-forums.com/index.php?topic=2086239.msg5479670#new'
				
					req = requests.get(URL)
				'''	

	with open('sublink_soup.html', 'r') as f_in:
		html = f_in.read()
	soup = BeautifulSoup(html, 'lxml')

	'''for i in soup.find_all('span', attrs = {'style': 'font-size:12pt'}):
					print(i)
			
				for i in soup.find_all('div', attrs = {'class': 'post', 'style': 'padding: 1ex 0;  margin-bottom: 0.5em;'}):
					print(i.text)'''
	#print(soup.find('span', attrs = {'style': 'font-size:12pt'}).text)
	'''for i, s in enumerate(soup.find_all('table', attrs = {'style': 'table-layout: fixed; width: 100%; height: auto !important;'})):
					print(i)
					print(s.text)'''

	x = soup.find('table', attrs = {'style': 'table-layout: fixed; width: 100%; height: auto !important;'})
	print(x.find('div', class_ = 'post').text)

	#print(soup.find('div', attrs = {'class': 'post', 'style': 'padding: 1ex 0;  margin-bottom: 0.5em;'}).text)
