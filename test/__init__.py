#! /usr/bin/python
# -*- coding: utf-8 -*-
from atexit import register as atexit_register
from contextlib import contextmanager
from pickle import dump, load
from os.path import abspath

from requests import Session

# Do not import library parts here. commons.py should not be loaded
# until LANG is set by test_fa and test_en.


FORCE_CACHE_OVERWRITE = False  # Use for updating cache entries
CHACHE_CHANGE = False
CACHE_PATH = abspath(__file__ + '/../.tests_cache')


# noinspection PyDecorator
@staticmethod
def fake_request(method, url, data=None, **kwargs):
    global CHACHE_CHANGE
    if data:
        cache_key = url + repr(sorted(data))
    else:
        cache_key = url
    response = cache.get(cache_key)
    if FORCE_CACHE_OVERWRITE or response is None:
        print('Downloading ' + url)
        with real_request():
            response = Session().request(
                method, url, data=data, **kwargs)
        cache[cache_key] = response
        CHACHE_CHANGE = True
    return response


def save_cache(cache_dict):
    """Save cache as pickle."""
    if not CHACHE_CHANGE:
        return
    print('saving new cache')
    with open(CACHE_PATH, 'wb') as f:
        dump(cache_dict, f)


def load_cache():
    """Return cache as a dict."""
    try:
        with open(CACHE_PATH, 'rb') as f:
            return load(f)
    except FileNotFoundError:
        return {}


def invalidate_cache(in_url):
    global CHACHE_CHANGE
    lower_url = in_url.lower()
    for k in cache.copy():
        if lower_url in k:
            del cache[k]
            CHACHE_CHANGE = True


@contextmanager
def real_request():
    Session.request = original_request
    yield
    Session.request = fake_request


original_request = Session.request
Session.request = fake_request


cache = load_cache()
# invalidate_cache('adine')
print('len(cache) ==', len(cache))
atexit_register(save_cache, cache)
