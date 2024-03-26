import mysql.connector
import pandas as pd
import requests
from bs4 import BeautifulSoup

host = "localhost"
user = "root"
password = "" # change
database = "lab4_v1" # change

connection = mysql.connector.connect(
	host=host,
	user=user,
	password=password,
	database=database
)

cursor = connection.cursor()

table_name = "reddit_posts"
content_check = "content"
corresponding_url = "url"

# check if values are empty / "missing"
#select_query = f"SELECT * FROM {table_name} WHERE {content_check} = '' " # IS NULL would not work
select_query = f"SELECT {content_check}, {corresponding_url} FROM {table_name} WHERE {content_check} = ''"

################## mysql portion ^ ##################


################## checks for empty cells via mysql ##################
df = pd.DataFrame()

try:
	cursor.execute(select_query)
	result = cursor.fetchall()
	if result:
		print(f"Values in '{content_check}' that are empty and their corresponding values in '{corresponding_url}':")
		for row in result:
			print(f"{row[0]} : {row[1]}")
		df = pd.DataFrame(result, columns=[content_check, corresponding_url])
		print(df)
	else:
		print(f"All values in column '{content_check}' are not NULL.")
except mysql.connector.Error as err:
		print(f"Error: {err}")

cursor.close()
connection.close()

################## local df ##################
#print(df)
urls = df['url']
print(urls)


def article_scraper(link):
	#print(link)
	url = link
	try:
		response = requests.get(url)
		if response.status_code == 200:
		    soup = BeautifulSoup(response.text, 'html.parser')
		    element = soup.find('title') #or find("body") #extract article content COMMENT THIS OUT TO GET ALL ARTICLE TEXT
		    #text = soup.findAll(text=True)
		    #text_content = element.get_text(' | ', strip=True) #extract article content COMMENT THIS OUT TO GET ALL ARTICLE TEXT
		    text_content = element.get_text()
		    print(text_content)
		    return text_content
		else:
		    #print(f"Failed to retrieve content. Status code: {response.status_code}")
		    error = f"Failed to retrieve content. Status code: {response.status_code}"
		return error
	except requests.exceptions.RequestException as e:
		# Handle exceptions (e.g., connection error, timeout, etc.)
		#print(f"Error accessing {url}: {e}")
		error = f"Error accessing {url}: {e}"
		return error



def check_YT(urls):
	url_content = [] # will need to add this to mysql !!!!!!!!!!!!!!!!!!!!!!!!!
	for u in urls:
		if "youtu.be" in u or "youtube.com" in u:
		#	print("YouTube video link")
			url_content.append("YouTube video link")
		elif "soundcloud" in u or "open.spotify" in u:
		#	print("Audio link")
			url_content.append("Audio link")
		else:
		#	print("***Possibly article link!!!")
			url_content.append(article_scraper(u))
	return url_content



df['new_content'] = check_YT(urls)
df.to_csv('./articlev_v3.csv')
