import investpy


def main():

    # Group issue #1 Issue 229
    # tester = investpy.get_stock_historical_data(stock='AAPL', country='United States')
    # print(tester)

    # Group issue #2 issue 203
    # data = investpy.get_indices_list(country='United States')
    # print(data)

    # Group issue #3 Issue 300
    # data = investpy.get_stock_financials(stock='GME', country='United States', finacials_type='BAL', totals_only=True)
    # print(data)

    # Alex Issue 291
    data = investpy.get_stock_financials(stock='GME', country='United States', finacials_type='BAL')
    print(data.columns)


    # Brandon issue 254
    # data = investpy.get_index_historical_data(index='Dow Jones US',
    #                                           country='united states',
    #                                           interval='Daily',
    #                                           from_date='01/01/1996',
    #                                           to_date='17/12/2020',
    #                                           order='descending')
    #
    # print(data.head())

    #Dennis Issue 339
    # df1 = investpy.search_quotes('LU0486851024', products=["etfs"], countries=["germany"])
    # df2 = investpy.search_quotes('IE00BFNM3P36', products=["etfs"], countries=["germany"])
    # print(df1)
    # print(df2)
    # search_results = investpy.search_quotes(text='apple',
    #                                         products=['stocks'],
    #                                         countries=['united states'],
    #                                         n_results=10)
    # for search_result in search_results[:1]:
    #     print(search_result)
    #     search_result.retrieve_historical_data(from_date='01/01/2019', to_date='01/01/2020')
    #     print(search_result.data.head())

    # Logan issue 284
    # data = investpy.technical_indicators(name='bbva', country='spain', product_type='stock', interval='daily')
    # data = investpy.technical_indicators(name='aapl', country='united states', product_type='stock', interval='daily')
    # data = investpy.technical_indicators(name='gme', country='united states', product_type='stock', interval='daily')
    # data = investpy.technical_indicators(name='U.S. 10Y', country='united states', product_type='bond', interval='daily')
    # data = investpy.technical_indicators(name='gme', country='united states', product_type='stock', interval='weekly')
    # print(data)

    # event = investpy.search_events(text="Japan M2 Money Stock Y2")
    # print(event)

if __name__ == '__main__':
    main()