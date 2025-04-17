

import requests 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up Chrome options




PATH_OF_WEBSITE = "https://edition.cnn.com/markets/fear-and-greed"
POSITION_PHRASE = 'id="extreme-fear"'


driver = webdriver.Chrome()
print("Driver initialized")
# Now you can use the driver just like before, but Chrome will run in the background without opening a window
driver.get(PATH_OF_WEBSITE)
print("Page loaded")
page_html = driver.page_source
print(page_html.find(POSITION_PHRASE)) # print the HTML content of the page

POSITION_INDEX = page_html.find(POSITION_PHRASE) 

filter_1 = page_html[POSITION_INDEX : POSITION_INDEX + 1300] # print the HTML content of the page
filter_2 = filter_1[filter_1.find('-number-value">') :filter_1.find('-number-value">') + 100 ] 
filter_3 = filter_2[filter_2.find('">')+2 : filter_2.find('<')]
print(filter_3) # print the HTML content of the page


# Close the browser
driver.quit()


#page_html = requests.get(PATH_OF_WEBSITE,headers = headers).text # string type returned




#print(page_html.find(POSITION_PHRASE)) # print the HTML content of the page

#POSITION_INDEX = page_html.find(POSITION_PHRASE) 

#filter_1 = page_html[POSITION_INDEX : POSITION_INDEX + 1300] # print the HTML content of the page
#filter_2 = filter_1[filter_1.find('-number-value">') :filter_1.find('-number-value">') + 100 ] 
#print(filter_2)