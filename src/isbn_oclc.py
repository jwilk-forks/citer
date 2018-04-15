#! /usr/bin/python
# -*- coding: utf-8 -*-
"""Define functions to process ISBNs and OCLC numbers."""

# from collections import defaultdict
from threading import Thread
from typing import Optional

from langid import classify
from regex import compile as regex_compile, DOTALL
from requests import get as requests_get

from config import ncbi_email, ncbi_tool
from src.adinebook import url2dictionary as adinebook_url2dictionary
from src.adinebook import isbn2url as adinebook_isbn2url
from src.bibtex import parse as bibtex_parse
from src.commons import dict_to_sfn_cit_ref  # , Name
from src.ris import parse as ris_parse


# original regex from:
# https://www.debuggex.com/r/0Npla56ipD5aeTr9
# https://www.debuggex.com/r/2s3Wld3CVCR1wKoZ
ISBN_10OR13_SEARCH = regex_compile(
    r'97[89]([ -]?+)(?=\d{1,5}\1?+\d{1,7}\1?+\d{1,6}\1?+\d)(?:\d\1*){9}\d'
    r'|(?=\d{1,5}([ -]?+)\d{1,7}\1?+\d{1,6}\1?+\d)(?:\d\1*+){9}[\dX]'
).search

ISBN10_SEARCH = regex_compile(
    r'(?=\d{1,5}([ -]?+)\d{1,7}\1?+\d{1,6}\1?+\d)(?:\d\1*+){9}[\dX]'
).search

ISBN13_SEARCH = regex_compile(
    r'97[89]([ -]?+)(?=\d{1,5}\1?+\d{1,7}\1?+\d{1,6}\1?+\d)(?:\d\1*+){9}\d'
).search


# original regex from: http://stackoverflow.com/a/14260708/2705757
# ISBN_REGEX = regex_compile(
#     r'(?=[-0-9 ]{17}|[-0-9X ]{13}|[0-9X]{10})(?:97[89][- ]?)'
#     r'?[0-9]{1,5}[- ]?(?:[0-9]+[- ]?){2}[0-9X]'
# )

OTTOBIB_SEARCH = regex_compile(
    '<textarea[^>]*+>(.*?)</textarea>',
    DOTALL,
).search

RM_DASH_SPACE = str.maketrans('', '', '- ')

CITOID_HEADERS = {
    'Api-User-Agent': ncbi_tool + '/' + ncbi_email,
}


class IsbnError(Exception):

    """Raise when bibliographic information is not available."""

    pass


def isbn_sfn_cit_ref(
    isbn_container_str: str, pure: bool=False, date_format: str='%Y-%m-%d'
) -> tuple:
    """Create the response namedtuple."""
    if pure:
        isbn = isbn_container_str
    else:
        # search for isbn13
        m = ISBN13_SEARCH(isbn_container_str)
        if m:
            isbn = m.group(0)
        else:
            # search for isbn10
            m = ISBN10_SEARCH(isbn_container_str)
            isbn = m.group(0)

    adinebook_result_list = []
    adine_book_thread = Thread(
        target=adinebook_thread_target,
        args=(isbn, adinebook_result_list),
    )
    adine_book_thread.start()

    citoid_result_list = []
    citoid_thread = Thread(
        target=citoid_thread_target,
        args=(isbn, citoid_result_list),
    )
    citoid_thread.start()

    ottobib_bibtex = ottobib(isbn)
    if ottobib_bibtex:
        otto_dict = bibtex_parse(ottobib_bibtex)
    else:
        otto_dict = None

    adine_book_thread.join()
    if adinebook_result_list:
        adine_dict = adinebook_result_list[0]
    else:
        adine_dict = None
    dictionary = choose_dict(adine_dict, otto_dict)

    citoid_thread.join()
    if citoid_result_list:
        dictionary['oclc'] = citoid_result_list[0]['oclc']

    dictionary['date_format'] = date_format
    if 'language' not in dictionary:
        dictionary['language'] = classify(dictionary['title'])[0]
    return dict_to_sfn_cit_ref(dictionary)


def adinebook_thread_target(isbn: str, result: list) -> None:
    """Append the dictionary generated by adinebook module to the result."""
    d = adinebook_url2dictionary(adinebook_isbn2url(isbn))
    if d:
        result.append(d)


def choose_dict(adine_dict, otto_dict):
    """Choose which source to use.

    Return adine_dict if both dicts contain the same ISBN.
    Return adine_dict if adine_dict is None.
    Return otto_dict otherwise.
    
    Note: AdineBook resolver removes 3 digits from ISBNs when converting
    them into URLs. This makes it vulnerable to resolving wrong ISBNs. Thus
    AdineBook should be passed as adine_dict.
    """
    if not otto_dict and not adine_dict:
        raise IsbnError('Bibliographic information not found.')
    if adine_dict and otto_dict:
        # both exist
        if isbn2int(adine_dict['isbn']) == isbn2int(otto_dict['isbn']):
            return adine_dict  # both isbns are equal
        return otto_dict  # isbns are not equal
    if adine_dict:
        return adine_dict  # only adinebook exists
    return otto_dict  # only ottobib exists


def isbn2int(isbn):
    return int(isbn.translate(RM_DASH_SPACE))


def get_citoid_dict(isbn) -> Optional[dict]:
    r = requests_get(
        'https://en.wikipedia.org/api/rest_v1/data/citation/mediawiki/' + isbn,
        headers=CITOID_HEADERS,
        timeout=10,
    )
    if r.status_code != 200:
        return
    return r.json()[0]
    # Currently get_citoid_dict is only used to get oclc id (T160845)
    # j0 = r.json()[0]
    # d = defaultdict(lambda: None, j0)
    # d['cite_type'] = j0['itemType']
    # d['isbn'] = d['ISBN'][0]
    # if 'date' in j0:
    #     d['year'] = j0['date']
    # if 'author' in j0:
    #     d['authors'] = [
    #         Name(first.rstrip('.,'), last.rstrip('.,'))
    #         for last, first in j0['author']
    #     ]
    # if 'url' in j0:
    #     del d['url']
    # if 'place' in j0:
    #     d['publisher-location'] = j0['place']
    # return d


def citoid_thread_target(isbn: str, result: list) -> None:
    citoid_dict = get_citoid_dict(isbn)
    if citoid_dict:
        result.append(citoid_dict)


def ottobib(isbn):
    """Convert ISBN to bibtex using ottobib.com."""
    m = OTTOBIB_SEARCH(
        requests_get(
            'http://www.ottobib.com/isbn/' + isbn + '/bibtex', timeout=10
        ).text
    )
    if m:
        return m[1]


def oclc_sfn_cit_ref(oclc: str, date_format: str='%Y-%m-%d') -> tuple:
    text = requests_get(
        f'https://www.worldcat.org/oclc/{oclc}?page=endnote'
        '&client=worldcat.org-detailed_record'
    ).text
    if '<html' in text:  # invalid OCLC number
        return (
            f'Error processing OCLC number: {oclc}',
            'Perhaps you entered an invalid OCLC number?',
            '',
        )
    d = ris_parse(text)
    authors = d['authors']
    if authors:
        # worldcat has a '.' the end of the first name
        d['authors'] = [(
            fn.rstrip('.') if not fn.isupper() else fn,
            ln.rstrip('.') if not ln.isupper() else ln,
        ) for fn, ln in authors]
    d['date_format'] = date_format
    d['oclc'] = oclc
    d['title'] = d['title'].rstrip('.')
    return dict_to_sfn_cit_ref(d)
