import investpy
import pandas as pd


def main():

    # data = investpy.get_stock_financial_summary(stock='GME', country='United States')
    # print(data.head())

    # temppls = investpy.get_stocks("United States")
    # print(temppls)

    # data = investpy.get_stock_financials(stock='AAPL', country='United States', finacials_type='BAL')
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

    data = investpy.get_stocks('India')
    pd.set_option('display.max_rows', None)
    print(data)


if __name__ == '__main__':
    main()

