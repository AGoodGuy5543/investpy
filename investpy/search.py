# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.
import json

import requests

from unidecode import unidecode

from .utils import constant as cst
from .utils.search_obj import SearchObj
from .utils.extra import random_user_agent

from lxml.html import fromstring


def search_quotes(text, products=None, countries=None, n_results=None):
    """
    This function will use the Investing.com search engine so to retrieve the search results of the
    introduced text. This function will create a :obj:`list` of :obj:`investpy.utils.search_obj.SearchObj`
    class instances which will contain the search results so that they can be easily accessed and so
    to ease the data retrieval process since it can be done calling the methods `self.retrieve_recent_data()`
    or `self.retrieve_historical_data(from_date, to_date)` from each class instance, which will fill the historical
    data attribute, `self.data`. The information of the financial product can also be retrieved using the
    function `self.retrieve_information()`, that will also dump the information in the attribute `self.info`.

    Args:
        text (:obj:`str`): text to search in Investing.com among all its indexed data.
        products (:obj:`list` of :obj:`str`, optional):
            list with the product type filter/s to be applied to search result quotes so that they match
            the filters. Possible products are: `indices`, `stocks`, `etfs`, `funds`, `commodities`, `currencies`, 
            `crypto`, `bonds`, `certificates` and `fxfutures`, by default this parameter is set to `None` which 
            means that no filter will be applied, and all product type quotes will be retrieved.
        countries (:obj:`list` of :obj:`str`, optional):
            list with the country name filter/s to be applied to search result quotes so that they match
            the filters. Possible countries can be found in the docs, by default this paremeter is set to
            `None` which means that no filter will be applied, and quotes from every country will be retrieved.
        n_results (:obj:`int`, optional): number of search results to retrieve and return.

    Returns:
        :obj:`list` of :obj:`investpy.utils.search_obj.SearchObj` or :obj:`investpy.utils.search_obj.SearchObj`:
            The resulting :obj:`list` of :obj:`investpy.utils.search_obj.SearchObj` will contained the retrieved
            financial products matching the introduced text if found, otherwise a RuntimeError will be raised, so as to
            let the user know that no results were found for the introduced text. But note that if the n_results value
            is equal to 1, a single value will be returned, instead of a list of values.

    Raises:
        ValueError: raised whenever any of the introduced parameter is not valid or errored.
        ConnectionError: raised whenever the connection to Investing.com failed.
        RuntimeError: raised when there was an error while executing the function.

    """

    if not text:
        raise ValueError('ERR#0074: text parameter is mandatory and it should be a valid str.')

    if not isinstance(text, str):
        raise ValueError('ERR#0074: text parameter is mandatory and it should be a valid str.')

    if products and not isinstance(products, list):
        raise ValueError(
            'ERR#0094: products filtering parameter is optional, but if specified, it must be a list of str.')

    if countries and not isinstance(countries, list):
        raise ValueError(
            'ERR#0128: countries filtering parameter is optional, but if specified, it must be a list of str.')

    if n_results and not isinstance(n_results, int):
        raise ValueError(
            'ERR#0088: n_results parameter is optional, but if specified, it must be an integer equal or higher than 1.')

    if n_results is not None:
        if n_results < 1:
            raise ValueError(
                'ERR#0088: n_results parameter is optional, but if specified, it must be an integer equal or higher than 1.')

    if products:
        try:
            products = list(map(lambda product: unidecode(product.lower().strip()), products))
        except:
            raise ValueError("ERR#0130: the introduced products filter must be a list of str in order to be valid.")

        condition = set(products).issubset(cst.PRODUCT_FILTERS.keys())
        if condition is False:
            # TODO: instead of printing the possible filters, reference the docs
            raise ValueError('ERR#0095: products filtering parameter possible values are: \"' + ', '.join(
                cst.PRODUCT_FILTERS.keys()) + '\".')

        products = [cst.PRODUCT_FILTERS[product] for product in products]
    else:
        products = list(cst.PRODUCT_FILTERS.values())

    if countries:
        try:
            countries = list(map(lambda country: unidecode(country.lower().strip()), countries))
        except:
            raise ValueError("ERR#0131: the introduced countries filter must be a list of str in order to be valid.")

        condition = set(countries).issubset(cst.COUNTRY_FILTERS.keys())
        if condition is False:
            # TODO: instead of printing the possible filters, reference the docs
            raise ValueError('ERR#0129: countries filtering parameter possible values are: \"' + ', '.join(
                cst.COUNTRY_FILTERS.keys()) + '\".')

        countries = [cst.COUNTRY_FILTERS[country] for country in countries]
    else:
        countries = list(cst.COUNTRY_FILTERS.values())

    params = {
        'search_text': text,
        'tab': 'quotes',
        'isFilter': True,
        'limit': 270,
        'offset': 0
    }

    head = {
        "User-Agent": random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    url = 'https://www.investing.com/search/service/SearchInnerPage'

    search_results = list()

    total_results = None

    while True:
        req = requests.post(url, headers=head, data=params)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        data = req.json()

        if data['total']['quotes'] == 0:
            raise RuntimeError("ERR#0093: no results found on Investing.com for the introduced text.")

        if total_results is None:
            total_results = data['total']['quotes']

        if n_results is None:
            n_results = data['total']['quotes']

        for quote in data['quotes']:
            country, pair_type = quote['flag'], quote['pair_type']

            if countries is not None:
                if quote['flag'] in countries:
                    country = cst.FLAG_FILTERS[quote['flag']]
                else:
                    continue

            if products is not None:
                if quote['pair_type'] in products:
                    pair_type = cst.PAIR_FILTERS[quote['pair_type']]
                else:
                    continue

            search_obj = SearchObj(id_=quote['pairId'], name=quote['name'], symbol=quote['symbol'],
                                   country=country, tag=quote['link'],
                                   pair_type=pair_type, exchange=quote['exchange'])

            # Solved search_quotes returns unconsistent type #339
            # if n_results == 1: return search_obj

            if search_obj not in search_results: search_results.append(search_obj)

        params['offset'] += 270

        if len(search_results) >= n_results or len(search_results) >= total_results or params[
            'offset'] >= total_results:
            break

    return search_results[:n_results]


def search_events(text, importances=None, countries=None, n_results=None):
    """
    TODO
    """

    if not text:
        raise ValueError('ERR#0074: text parameter is mandatory and it should be a valid str.')

    if not isinstance(text, str):
        raise ValueError('ERR#0074: text parameter is mandatory and it should be a valid str.')

    if importances and not isinstance(importances, list):
        raise ValueError(
            'ERR#0138: importances filtering parameter is optional, but if specified, it must be a list of str.')

    if countries and not isinstance(countries, list):
        raise ValueError(
            'ERR#0128: countries filtering parameter is optional, but if specified, it must be a list of str.')

    if n_results and not isinstance(n_results, int):
        raise ValueError(
            'ERR#0088: n_results parameter is optional, but if specified, it must be an integer equal or higher than 1.')

    if n_results is not None:
        if n_results < 1:
            raise ValueError(
                'ERR#0088: n_results parameter is optional, but if specified, it must be an integer equal or higher than 1.')

    text_alt = text.replace(' ', '%20')

    params = {
        'search_text': text_alt,
        'tab': 'ec_event',
        'limit': 270,
        'offset': 0
    }

    headers = {
        "User-Agent": random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    # text_alt = text.replace(' ', '%20')
    # text_alt = text_alt + "&tab=ec_event"
    # url = "https://www.investing.com/search/?q=" + text + "&tab=ec_event"
    url = 'https://www.investing.com/search/service/SearchInnerPage'

    search_results = list()

    total_results = None

    while True:
        response = requests.post(url, data=params, headers=headers)

        if response.status_code != 200:
            raise ConnectionError(f"ERR#0015: error {response.status_code}, try again later.")

        # resp_dict = json.load(response.text)

        # print(json.dumps(response.text))
        events = response.json()['ec_event']

        if len(events) == 0:
            raise RuntimeError("ERR#0093: no results found on Investing.com for the introduced text.")

        print(text)
        for returned in events:
            if returned["searchable"] == text:
                target_url = "https://www.investing.com" + returned["link"]

        response_economic = requests.post(target_url, data=params, headers=headers)

        if response.status_code != 200:
            raise ConnectionError(f"ERR#0015: error {response.status_code}, try again later.")

        root = fromstring(response_economic.text)

        table = root.xpath(".//table[contains(@class, 'genTbl openTbl ecHistoryTbl')]/tbody/tr")

        for row in table:
            counter = 0
            for value in row.xpath("td"):
                print(value.text)
                counter = counter + 1
        break

# def search_events(text, importances=None, countries=None, n_results=None):
#     """
#     TODO
#     """
#
#     if not text:
#         raise ValueError('ERR#0074: text parameter is mandatory and it should be a valid str.')
#
#     if not isinstance(text, str):
#         raise ValueError('ERR#0074: text parameter is mandatory and it should be a valid str.')
#
#     if importances and not isinstance(importances, list):
#         raise ValueError('ERR#0138: importances filtering parameter is optional, but if specified, it must be a list of str.')
#
#     if countries and not isinstance(countries, list):
#         raise ValueError('ERR#0128: countries filtering parameter is optional, but if specified, it must be a list of str.')
#
#     if n_results and not isinstance(n_results, int):
#         raise ValueError('ERR#0088: n_results parameter is optional, but if specified, it must be an integer equal or higher than 1.')
#
#     if n_results is not None:
#         if n_results < 1:
#             raise ValueError('ERR#0088: n_results parameter is optional, but if specified, it must be an integer equal or higher than 1.')
#
#     params = {
#         'search_text': text,
#         'tab': 'ec_event',
#         'limit': 270,
#         'offset': 0
#     }
#
#     headers = {
#         "User-Agent": random_user_agent(),
#         "X-Requested-With": "XMLHttpRequest",
#         "Accept": "text/html",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Connection": "keep-alive",
#     }
#
#     print(text)
#     text_alt = text.replace(' ', '%20')
#     text_alt = text_alt + "&tab=ec_event"
#     url = "https://www.investing.com/search/?q=" + text_alt
#     print(url)
#
#     # search_results = list()
#     #
#     # total_results = None
#
#     # while True:
#     response = requests.post(url, data=params, headers=headers)
#     tester = fromstring(response.text)
#     print(tester)
