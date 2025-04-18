

import requests 
import interactive_broker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up Chrome options
PATH_OF_WEBSITE = "https://edition.cnn.com/markets/fear-and-greed"
POSITION_PHRASE = 'id="extreme-fear"'  # we would find the FEAR INDEX after this tag , which is identified by a unique ID 
def get_html_page():
    driver = webdriver.Chrome()        # we need web Driver to open google chrome via python program
    print("Driver initialized")
    # Now you can use the driver just like before, but Chrome will run in the background without opening a window
    driver.get(PATH_OF_WEBSITE)
    print("Page loaded")
    page_html = driver.page_source  # get the HTML content of the page
    driver.quit()
    return page_html 
def get_greed_fear_index(page_html):
    POSITION_INDEX = page_html.find(POSITION_PHRASE) 

    filter_1 = page_html[POSITION_INDEX : POSITION_INDEX + 1300]    # these filters would reduce the scope , till we get the number value of the fear index 
    filter_2 = filter_1[filter_1.find('-number-value">') :filter_1.find('-number-value">') + 100 ] 
    filter_3 = filter_2[filter_2.find('">')+2 : filter_2.find('<')]
    print(filter_3) # print the HTML content of the page


    greed_fear_number = int(filter_3) # convert the string to an integer
    return greed_fear_number
# Close the browser
def find_a_trade_to_sell(database_file,current_price, profit_percentage):
    data = get_json_data()
    amount_of_shares_to_sell = 0 
    for key , listt in data.items() :
        if not listt[3] :    # this enter hasn't been sold
            price = listt[0]
            quantity = listt[1]
            if price > current_price and (( current_price - price )/ price) * 100 >= profit_percentage :
                amount_of_shares_to_sell += quantity
                data[key][3] = True 
                data[key][4] = (( current_price - price )/ price) * 100 # profit gained in this trade 
    return amount_of_shares_to_sell                     
async def main() :
    
    # once every 3 hours , we run this program 
    html = get_html_page() 
    greed_fear_number = get_greed_fear_index(html)
    ib = connect_to_ibkr()
    price = get_current_price_of_HLAL(ib)
    
    if greed_fear_number <= 15 :
        # GOAL   :    buy , then store the price + amount we bought
        # connect to the exchange API 
        account_balance = await get_account_balance(ib)
        # buy 20% of the account balance if 1 stock > 20% of the account balance
        amount_invested_in_trade = account_balance if account_balance >= price else return
        if account_balance >= 5 * price :
            amount_invested_in_trade = account_balance / 5 # enter only a fifth 
        number_of_stocks_going_to_buy = amount_invested_in_trade // price
        await buy_HLAL(ib,number_of_stocks_going_to_buy) # buys then stores at this line
        # store the price and amount bought in txt file 
        
        print(f"buy at {price} with {number_of_stocks_goint_to_buy} stocks")
        
        
    if greed_fear_number >= 85 :
        # GOAL : sell ONLY if we are profitable , then store the profit gained ... 
        amount_of_shares_to_sell = find_a_trade_to_sell(database_file, price , 20 )
        # find a trade in the json file , that if sold we would be profitable 
        # sell the trade 
        if amount_of_shares_to_sell > 0 :
            await sell_HLAL(ib,amount_of_shares_to_sell)
        # store the profit gained in json file
        
            print(f"sell at {price} with {amount_of_shares_to_sell} stocks")
### for other developers to do : send notifications to the owner in telegram on any update   ###


async def schedular():
    while 1 :
        await main() 
        await asyncio.sleep(3 * 60 * 60) # run the main() once every 3 hours , to reduce the bandwidth usage 


if __name__ == "__main__":
    asyncio.run(schedular())

