import requests
from bs4 import BeautifulSoup
import sys
import os
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


def get_soup(URL):
	req = requests.get(URL)
	STATUS_CODE = req.status_code

	if STATUS_CODE == 200:
		soup = BeautifulSoup(req.text, 'lxml')

		return soup

	if STATUS_CODE == 404:
		print('BAD REQUEST!')

		sys.exit(1)

def get_links(soup):

	href_set = set()

	tr_list = soup.find_all('tr', class_='related')

	if tr_list:
		for box in tr_list:
			a_list = box.find_all('a', href=True)

			for a in a_list:
				href_set.add(a['href'])

	return href_set

def login(LOGIN_PAGE, USERNAME, PASSWORD):

	wait = WebDriverWait(driver, 15)

	print('Getting login page')
	driver.get(LOGIN_PAGE)

	print('Waiting for cover to go away')
	wait.until(EC.invisibility_of_element((By.ID, "loading-bg")))

	print('Inputting login fields')
	username = driver.find_element(By.NAME, "user")
	password = driver.find_element(By.NAME, "passwrd")

	username.send_keys(USERNAME)
	password.send_keys(PASSWORD)

	login_button = driver.find_element(By.XPATH, '//button[contains(text(),"Log In")]')
	login_button.click()

	print('Logged In')

def setup_driver(chrome_path):
	options = Options()
	options.add_argument('--headless') # headless mode to reduce load
	options.add_argument('--disable-gpu') # to reduce load even more
	service = Service(executable_path=chrome_path)
	return webdriver.Chrome(options=options, service=service)

def keep_before_word(s, word):

	i = s.find(word)

	if i != -1:
		return s[:i]
	else:
		return s

def get_QNA(link):

	print(f'Nav to {link}')
	driver.get(link)

	try:
		WebDriverWait(driver, 10).until(
		    EC.presence_of_element_located((By.TAG_NAME, "body"))
		)

		try: 
			click_XPATH = "//a[contains(text(), 'Click to Unlock Response')]"
			link = driver.find_element(By.XPATH, click_XPATH)
			link.click()
			print("Link found and clicked.")
		except NoSuchElementException:
			pass

		"""
		BeautifulSoup the page and find Question and Answer
		"""
		page_source = driver.page_source
		sublink_soup = BeautifulSoup(page_source, 'lxml')


		''' UNCOMMENT TO USE 

		with open('sublink_soup.html', 'w') as f_out:
									f_out.write(str(sublink_soup))'''

		question = sublink_soup.find('span', attrs = {'style': 'font-size:12pt'})

		question_str = question.text if question else ''

		answer = sublink_soup.find('div', attrs = {'class': 'post', 'style': 'padding: 1ex 0px; margin-bottom: 0.5em; height: auto !important;'})

		answer_str = answer.text if answer else ''
		if answer_str:
			answer_str = keep_before_word(answer_str, 'Answer unlocked!').replace('\n', '')

		print('Success!')
		return (question_str, answer_str)

	except Exception as e:
		print("An error occurred:", e)
		print('Skipping link!')
		return (link, '')

if __name__ == '__main__':

	URL = 'https://biology-forums.com/index.php?board=84.0'

	LOGIN_PAGE = 'https://biology-forums.com/index.php?action=login'
	USERNAME = 'nealsons@usc.edu'
	PASSWORD = 'pharmaIsCool'

	CHROME_DRIVER_PATH = '/usr/bin/chromedriver'

	print('Getting links')
	soup = get_soup(URL)
	href_set = get_links(soup)
	href_set.remove('javascript:;')
	href_set = {href for href in href_set if 'profile' not in href}
	href_set = {keep_before_word(href, '.msg').replace('\n', '').replace('.0', '') for href in href_set}
	href_set = sorted(list(href_set))

	'''login_soup = get_soup(LOGIN_PAGE)
				with open('login.html', 'w') as f_out:
					f_out.write(str(login_soup))'''

	with open('sublinks.txt', 'w') as f_out:
		for i in href_set:
			f_out.write(f'{i}\n')

	print('Setting up WebDriver')
	driver = setup_driver(CHROME_DRIVER_PATH)

	print('Logging in')
	login(LOGIN_PAGE, USERNAME, PASSWORD)

	QNA_list = []
	for href in href_set:
		QNA_tuple = get_QNA(href)
		QNA_list.append(QNA_tuple)

	OUT_PATH = 'QNA.txt'
	print(f'Outputting to {OUT_PATH}')
	with open(OUT_PATH, 'w') as f_out:
		f_out.write('Question,Answer\n')

		for q, a in QNA_list:
			f_out.write(f'{q},{a}\n')

	driver.quit()



