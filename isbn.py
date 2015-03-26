#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Codes specifically related to ISBNs."""

import re

import requests
import threading

import commons
import bibtex
import adinebook


# original regex from: https://www.debuggex.com/r/0Npla56ipD5aeTr9
ISBN13_REGEX = re.compile(
    r'97(?:8|9)([ -]?)(?=\d{1,5}\1?\d{1,7}\1?\d{1,6}\1?\d)(?:\d\1*){9}\d'
)
# original regex from: https://www.debuggex.com/r/2s3Wld3CVCR1wKoZ
ISBN10_REGEX = re.compile(
    r'(?=\d{1,5}([ -]?)\d{1,7}\1?\d{1,6}\1?\d)(?:\d\1*){9}[\dX]'
)
# original regex from: http://stackoverflow.com/a/14260708/2705757
ISBN_REGEX = re.compile(
    r'(?=[-0-9 ]{17}|[-0-9X ]{13}|[0-9X]{10})(?:97[89][- ]?)'
    r'?[0-9]{1,5}[- ]?(?:[0-9]+[- ]?){2}[0-9X]'
)


class IsbnError(Exception):

    """Raise when bibliographic information is not available."""

    pass


class Response(commons.BaseResponse):

    """Create isbn's response object."""

    def __init__(self, isbn_container_string, pure=False,
                 date_format='%Y-%m-%d'):
        """Make the dictionary and run self.generate()."""
        self.date_format = date_format
        if pure:
            self.isbn = isbn_container_string
        else:
            # search for isbn13
            m = ISBN13_REGEX.search(isbn_container_string)
            if m:
                self.isbn = m.group(0)
            else:
                # search for isbn10
                m = ISBN10_REGEX.search(isbn_container_string)
                self.isbn = m.group(0)
        self.bibtex = ottobib(self.isbn)
        adinebook_dict_list = []
        thread = threading.Thread(
            target=adinebook_thread,
            args=(self.isbn, adinebook_dict_list),
        )
        thread.start()
        if self.bibtex:
            otto_dict = bibtex.parse(self.bibtex)
        else:
            otto_dict = None
        thread.join()
        if adinebook_dict_list:
            adine_dict = adinebook_dict_list.pop()
        else:
            adine_dict = None
        self.dictionary = choose_dict(adine_dict, otto_dict)
        if 'language' not in self.dictionary:
            self.detect_language(self.dictionary['title'])
        self.generate()


def adinebook_thread(isbn, result_list):
    """Add the dictionary generated by adinebook module to the result_list."""
    result_list.append(
        adinebook.url2dictionary(
            adinebook.isbn2url(isbn)
        )
    )


def choose_dict(adine_dict, otto_dict):
    """Choose which source to use.

    Return adinebook if both contain the same ISBN or if adinebook is None,
    else return ottobib.
    
    Background: adinebook.com ommits 3 digits from it's isbn when converting
    them to URLs. This may make them volnarable to resolving into wrong ISBN.
    """
    if not otto_dict and not adine_dict:
        raise IsbnError('Bibliographic information not found.')
    elif adine_dict and otto_dict:
        # both exist
        if isbn2int(adine_dict['isbn']) == isbn2int(otto_dict['isbn']):
            # both isbns are equal
            return adine_dict
        else:
            # isbns are not equal
            return otto_dict
    elif adine_dict:
        # only adinebook exists
        return adine_dict
    else:
        # only ottobib exists
        return otto_dict


def isbn2int(isbn):
    """Get ISBN string and return it as in integer."""
    isbn = isbn.replace('-', '')
    isbn = isbn.replace(' ', '')
    return int(isbn)


def ottobib(isbn):
    """Convert ISBN to bibtex using ottobib.com."""
    ottobib_url = 'http://www.ottobib.com/isbn/' + isbn + '/bibtex'
    ottobib_html = requests.get(ottobib_url).text
    m = re.search('<textarea.*>(.*)</textarea>', ottobib_html, re.DOTALL)
    if m:
        return m.group(1)
