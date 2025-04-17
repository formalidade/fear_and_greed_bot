

import requests 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--disable-gpu')  # Disable GPU (optional, but can help with some issues)
options.add_argument('--no-sandbox')


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0'
}


PATH_OF_WEBSITE = "https://edition.cnn.com/markets/fear-and-greed"
POSITION_PHRASE = 'id="extreme-fear"'


driver = webdriver.Chrome(options=options)

# Now you can use the driver just like before, but Chrome will run in the background without opening a window
driver.get(PATH_OF_WEBSITE)

greedfear_element = driver.find_element(By.ID, 'extreme-fear')

subsequent_elements = greedfear_element.find_elements(By.XPATH, 'following-sibling::*')



page_html = requests.get(PATH_OF_WEBSITE,headers = headers).text # string type returned




print(page_html.find(POSITION_PHRASE)) # print the HTML content of the page

POSITION_INDEX = page_html.find(POSITION_PHRASE) 

filter_1 = page_html[POSITION_INDEX : POSITION_INDEX + 1300] # print the HTML content of the page
filter_2 = filter_1[filter_1.find('-number-value">') :filter_1.find('-number-value">') + 100 ] 
print(filter_2)