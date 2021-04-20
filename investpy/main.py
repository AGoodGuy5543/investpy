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

    # data = investpy.get_stock_financials(stock='AAPL', country='United States')
    # print("Before")
    # print(data)
    # print("After")

    # tester = investpy.get_stock_historical_data(stock='AAPL', country='United States')
    # print(tester)

    # data = investpy.technical_indicators(name='bbva', country='spain', product_type='stock', interval='daily')
    # data = investpy.technical_indicators(name='aapl', country='united states', product_type='stock', interval='daily')
    # data = investpy.technical_indicators(name='gme', country='united states', product_type='stock', interval='daily')
    # data = investpy.technical_indicators(name='U.S. 10Y', country='united states', product_type='bond', interval='daily')
    # data = investpy.technical_indicators(name='gme', country='united states', product_type='stock', interval='weekly')

    # print(data)
    # data = investpy.get_index_recent_data(index='ibex 35', country='spain')
    # group issue 2 print(investpy.get_stocks())

    data = investpy.get_index_historical_data(index='Dow Jones US',
                                              country='united states',
                                              interval='Daily',
                                              from_date='01/01/1996',
                                              to_date='17/12/2020',
                                              order='descending',
                                              as_json=True)

    print(data.head())

    # data = investpy.get_indices_list(country='United States')
    # print(data)



if __name__ == '__main__':
    main()
