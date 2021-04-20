import investpy
import pandas as pd

# tester = investpy.get_stock_historical_data(stock='AAPL', country='United States')

# tester = investpy.get_stock_financials(stock='AAPL', country='United States')

# Dennis's Problem got rid of if statement
search_results = investpy.search_quotes(text='apple',
                                       products=['stocks'],
                                       countries=['united states'],
                                       n_results=10)
for search_result in search_results[:1]:
    print(search_result)
    search_result.retrieve_historical_data(from_date='01/01/2019', to_date='01/01/2020')
    print(search_result.data.head())


# df1 = investpy.search_quotes('LU0486851024',products=["etfs"],countries=["germany"])
# df2 = investpy.search_quotes('IE00BFNM3P36',products=["etfs"],countries=["germany"])
# for result in df1[:1]:
#     print(result)

#print(investpy.get_stocks())
