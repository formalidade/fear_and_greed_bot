from ib_async import *

database_file = 'trades.json'

async def connect_to_ibkr():
    # Connect to IBKR API
    ib = IB()

    await ib.connect('127.0.0.1', 7497, clientId=1)
    
    return ib


async def get_current_price_of_HLAL(ib):
    # Get the current price of HLAL
    contract = Stock('HLAL', 'ARCA', 'USD')
    await ib.reqMktData(contract)
   
    ticker = ib.ticker(contract)

    current_price = ticker.last  # Get the current price
    return float(current_price)

async def get_account_balance(ib):
    account_summary = await ib.accountSummary()

    # Find BuyingPower entry
    buying_power = next((item for item in account_summary if item.tag == 'BuyingPower'), None)

    # Print it
    if buying_power:
        print(f"Buying Power: {buying_power.value} {buying_power.currency}")
        return buying_power.value
    else:
        print("Buying Power not available.")
        return False 


async def buy_HLAL(ib, amount_to_invest):
    # Buy HLAL stock
    contract = Stock('HLAL', 'ARCA', 'USD')
    order = MarketOrder('BUY', amount_to_invest)
    
    trade = await ib.placeOrder(contract, order)
    store_buy_trade(database_file , trade) 
    return trade



async def sell_HLAL(ib, amount_to_sell):
    # Sell HLAL stock
    contract = Stock('HLAL', 'ARCA', 'USD')
    
    order = MarketOrder('SELL', amount_to_sell)
    
    await trade = ib.placeOrder(contract, order)
    # Wait until order is completely filled
    while trade.orderStatus.status != 'Filled':
        await ib.sleep(1)  # Wait for 1 second before checking again
    
    
    modify_sold_trades(trade)  # fills the buy orders in our database (FIFO) 
    
    
    return trade

def modify_sold_trades(trade):
        data = get_json_data():
        total_shares_sold = 0 
        total_value = 0
        for fill in trade.fills:
            shares = fill.execution.shares
            price = fill.execution.price
        
            total_shares_sold += shares
            total_value += shares * price
        temp_quantity = total_shares_sold
        avg_price = total_value / total_shares_sold if total_shares_sold > 0 else 0
        # explanation of the following code : The function matches sold shares from a trade to previously bought (unsold) trades stored in a dictionary. It loops through fills to track total shares sold, then:
        
        # If enough shares were sold to fully cover a previous buy:

            # Mark it as sold

            # Calculate profit/loss as a percentage

            # Subtract the used quantity
            
        #If only part of a previous buy is covered:

            #Mark it as sold

            #Reduce the quantity in that buy entry

            #Assign remaining sold shares accordingly

    #       ✅ Break early when all sold shares are allocated.
        
        
        for key , value in data.items():
            if not value[3] and temp_quantity >= value[1] : # not sold 
                data[key][3]  = True 
                data[key][4]  = (( value[0] - price )/ price) * 100
                temp_quantity -= value[1] 
            if temp_quantity < value[1] and not value[3]:  # this should be 
                data[key][3]  = True 
                data[key][4]  = (( value[0] - price )/ price) * 100
                data[key][1] = data[key][1] - temp_quantity 
                temp_quantity = 0 
            if value[3] and temp_quantity == 0 :
                break
        store_json_data(data)
                
        
        
        
    
    
def store_buy_trade(database , trade):
   
  
            # Get fill info
            fill = trade.fills[0]  # assuming only one fill
            price = fill.execution.price
            date_bought = fill.execution.time
            shares = fill.execution.shares 
            # Store in file
            data = get_json_data()
                
            trade_id = f"trade_{len(data)}"

            data['trade'+trade_id] = [price,shares , date_bought,False,0] # format [priceBought,Quantity,date,isSold,ProfitIfsold] -> (int , int , ? , boolean , int) 
            
            store_json_data(data)  
                       
def get_json_data():
            data = dict()
            try:
                with open(database, 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                print("File not found!")
                
            except json.JSONDecodeError:
                print("Invalid JSON format!")
            return data
       
def store_json_data(dictionary) :
            with open(database, 'w') as file:
                json.dump(dictionary, file, indent=4)
    