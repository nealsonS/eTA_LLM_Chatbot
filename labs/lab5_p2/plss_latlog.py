import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import mysql.connector
import time

def get_user_password():
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'
    password = input("Please enter your MySQL password:\n")
    return user, password

def connect_to_database(host, user, password, database):
    try:
        return mysql.connector.connect(host=host, user=user, password=password, database=database)
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        sys.exit(1)

def get_PLSS(data):

	URL = 'https://www.dmr.nd.gov/oilgas/findwellsvw.asp?'
	op_api = {}

	for x in data:
		api = x[0]
		op = x[1]

		op_api.setdefault(op, [])
		op_api[op].append(api)

	if None in op_api:
		del op_api[None]

	loc_set = set()
	for op, api_list in op_api.items():
		session = requests.Session()

		api_in_op = [api.replace('-', '') for api in op_api[op]]

		form = {
		'ddmOperator': op
		}

		res = session.post(URL, data=form)
		soup = BeautifulSoup(res.text, 'html.parser')
		table = soup.find('table', attrs={'summary': 'Well Log search results table'})

		# extract api to location keypair => (api, loc)
		if table:
			api_loc = {}
			rows = table.find_all('tr')
			for i, row in enumerate(rows):
				if i != 0:
					cells = row.find_all('td')
					row_api= cells[2].text.strip()
					row_loc = cells[7].text.strip()

					if row_api in api_in_op:
						loc_set.add((row_api, row_loc))
			print(f'Success in obtaining PLSS data for: {op}')

		if not table:
			print(f"Failed to find table for Operator: {op}")

	return loc_set

def conv_PLSS_latlong(plss_data):

	URL = 'https://www.earthpoint.us/TownshipsSearchByDescription.aspx'
	STATE = 'ND'
	MERIDIAN = '05'
	BUTTON_ID = 'ContentPlaceHolder1_btnTownshipView'

	'''	# get cookies
	session = requests.Session()
	res = session.get('https://www.earthpoint.us/TownshipsSearchByDescription.aspx')
	headers = {
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
	    'Content-Type': 'application/x-www-form-urlencoded'
	}
	session.headers.update(headers)
	session.get(URL)'''

	driver = webdriver.Chrome()
	driver.get(URL)

	'''	ddstate = Select(driver.find_element('id', 'ContentPlaceHolder1_State'))
	ddmeri = Select(driver.find_element('id', 'ContentPlaceHolder1_Meridian'))
	ddtown = Select(driver.find_element('id', 'ContentPlaceHolder1_Township'))
	ddran = Select(driver.find_element('id', 'ContentPlaceHolder1_Range'))
	ddsec = Select(driver.find_element('id', 'ContentPlaceHolder1_Section'))'''

	view_button = driver.find_element('id', BUTTON_ID)
	c = 0
	for api, loc in plss_data:
		if c in [0]:
			loc_values = loc.split()[1].strip().split('-')
			TOWNSHIP = loc_values[1].strip() + ';0;N'
			RANGE = loc_values[2] + ';0;W'
			SECTION = loc_values[0]
			if len(SECTION) == 2:
				SECTION = '0' + SECTION

			form = {
				'ContentPlaceHolder1_State': STATE,
				'ContentPlaceHolder1_Meridian': MERIDIAN,
				'ContentPlaceHolder1_Township': TOWNSHIP,
				'ContentPlaceHolder1_Range': RANGE,
				'ContentPlaceHolder1_Section': SECTION
			}

			#res = session.post(URL, data=form)

			#soup = BeautifulSoup(res.text, html.parser)
			try:
				for key, val in form.items():
					dropdown = Select(driver.find_element('id', key))
					opt = dropdown.options
					for i in opt:
						print(i.text)
					dropdown.select_by_value(val)
					WebDriverWait(driver, 5)

				view_button.click()
				with open('out_test.html', 'w') as f_out:
					f_out.write(driver.page_source)

			except NoSuchElementException as e:
				print('Option not valid!')



			#time.sleep(3)
		c = c + 1
	#driver.quit()






if __name__ == '__main__':

    host = 'localhost'
    user, password = get_user_password()
    database = input("Please enter your MySQL database:\n")
    
    connection = connect_to_database(host, user, password, database)
    print("Connected to the database.")
    cursor = connection.cursor()

    # Fetch api number and operator numbers
    cursor.execute("SELECT api_number, operator FROM well_data")
    data = cursor.fetchall()

    PLSS_list = get_PLSS(data)
    conv_PLSS_latlong(PLSS_list)

