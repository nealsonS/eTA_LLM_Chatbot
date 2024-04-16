## wikipedia_scraper.py
1. Scrape raw HTML
2. Soup the main file
3. Go to the `Branches` section and visit each href link
- Also use each description as the summary for each href link
4. Soup each href's body paragraphs
5. Scrape all paragraphs
6. Output to Wikip.txt


## bio_forum.py
Scraper for url: https://biology-forums.com/index.php?board=84.0
1. Collect all subforums of main page using requests
2. Login using credentials using selenium
3. For every subforum, collect the question and answer
4. Output for QNA.txt

### Requirements
The code uses chromium browser and its chromedriver for selenium. So please install by running this in terminal:
```
sudo apt-get install chromium-chromedriver
# DISCLAIMER: THIS WILL INSTALL CHROMIUM BROWSER
```
Also: 
```
pip install selenium
pip install lxml
```
