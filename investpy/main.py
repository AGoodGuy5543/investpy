import investpy

# df = investpy.get_stock_historical_data(stock='AAPL',
#                                         country='United States',
#                                         from_date='01/01/2010',
#                                         to_date='01/01/2020')

tester = investpy.get_stock_historical_data(stock='AAPL', country='United States')

print(tester)