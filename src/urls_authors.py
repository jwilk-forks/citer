#! /usr/bin/python
# -*- coding: utf-8 -*-

"""This module is used for finding the authors in a soup object.

It is in urls.py.
"""


from re import compile as re_compile, IGNORECASE
from typing import Optional, List

import regex

from src.commons import ANYDATE_SEARCH, RawName, InvalidNameError, Name


# Names in byline are required to be two or three parts
NAME_PATTERN = r'(?>\w[\w.-]+\ )(?>\w[\w.-]+)(?>\ \w[\w.-]+)?'

# BYLINE_PATTERN supports up to four names in a byline
# names may be separated with "and", a "comma" or "comma and"
BYLINE_PATTERN = rf'''
    \s*By\s+{NAME_PATTERN}(
        ,\ {NAME_PATTERN}(
            ,\ {NAME_PATTERN}(
                ,\ {NAME_PATTERN}
                |
                ,?\ +and\ {NAME_PATTERN}
            )?
            |
            ,?\ +and\ {NAME_PATTERN}(
                ,\ {NAME_PATTERN}
                |
                ,?\ +and\ {NAME_PATTERN}
            )?
        )?
        |
        ,?\ +and\ {NAME_PATTERN}(
            ,\ {NAME_PATTERN}(
                ,\ {NAME_PATTERN}
                |
                ,?\ +and\ {NAME_PATTERN}
            )?
            |
            ,?\ +and\ {NAME_PATTERN}(
                ,\ {NAME_PATTERN}
                |
                ,?\ +and\ {NAME_PATTERN}
            )?
        )?
    )?\s*
'''
BYLINE_PATTERN_SEARCH = regex.compile(BYLINE_PATTERN, regex.X | regex.I)

NORMALIZE_ANDS = re_compile(r'\s+and\s+', IGNORECASE).sub
NORMALIZE_COMMA_SPACES = re_compile(r'\s*,\s+', IGNORECASE).sub
BY_PREFIX = re_compile(
    r'^(?:[\s\S]*?\bby\s+)?([^\r\n]+)[\s\S]*',
    IGNORECASE,
).sub
AND_OR_COMMA_SUFFIX = re_compile(r'(?: and|,)?\s*$', IGNORECASE).sub
AND_OR_COMMA_SPLIT = re_compile(r', and | and |, |;', IGNORECASE).split
AND_SPLIT = re_compile(r', and | and |;', IGNORECASE).split

CONTENT_ATTR = r'content=(?<q>["\'])\s*(?<result>.*?)\s*(?P=q)'
AUTHOR_META_NAME_OR_PROP = r'''
    (?<id>(?:name|property)\s*=\s*(?<q>["\'])
        (?>
            # http://socialhistory.ihcs.ac.ir/article_571_84.html
            # http://jn.physiology.org/content/81/1/319
            a(?>rticle:author|uthor)
            |citation_authors?
            |og:author
        )
    (?P=q))
'''
META_AUTHOR_FINDITER = regex.compile(
    rf'''
    <meta\s[^>]*?(?:
        {AUTHOR_META_NAME_OR_PROP}\s[^>]*?{CONTENT_ATTR}
        |
        {CONTENT_ATTR}\s[^>]*?{AUTHOR_META_NAME_OR_PROP}
    )
    ''',
    regex.VERBOSE | regex.IGNORECASE
).finditer
# id=byline
# http://www.washingtonpost.com/wp-dyn/content/article/2006/12/20/AR2006122002165.html
# rel=author
# http://timesofindia.indiatimes.com/india/27-ft-whale-found-dead-on-Orissa-shore/articleshow/1339609.cms?referral=PM
BYLINE_TAG_FINDITER = regex.compile(
    rf'''
    (?>
        # author_byline example:
        # http://blogs.ft.com/energy-source/2009/03/04/the-source-platts-rocks-boat-300-crude-solar-shake-ups-hot-jobs/#axzz31G5iiTSq
        # try byline before class_='author'
        <(?<tag>[a-z]\w+)\s+[^>]*?
        (?<id>
            (?>class|id|rel)=(?<q>["\'])
                (?>
                    author(?>_byline|Inline|-title)?
                    |by(?>
                        line(?>Author|line-name)?
                        |_line(?:_date)?
                    )
                    |meta-author
                    |story-byline
                )
            )
        (?P=q)[^>]*?>(?<result>[\s\S]*?)</(?P=tag)(?>[^>]*)>
        |
        # http://www.dailymail.co.uk/news/article-2633025/London-cleric-convicted-NYC-terrorism-trial.html
        (?<id>authorName["\']?\s*:\s*["\'])(?<result>[^"\'>\n]+)["\']
        |
        # schema.org
        (?<q>["'])author(?P=q)\s*:\s*{{\s*(?P=q)@type(?P=q)\s*:\s*(?P=q)
        (?<id>Person)(?P=q)\s*,\s*(?P=q)name(?P=q)\s*:\s*(?P=q)(?<result>.*?)(?P=q)
    )
    ''',
    regex.VERBOSE | regex.IGNORECASE | regex.ASCII,
).finditer


BYLINE_HTML_PATTERN = regex.compile(
    rf'>{BYLINE_PATTERN}<', regex.VERBOSE | regex.IGNORECASE
).search
# [\n|]{BYLINE_PATTERN}\n
# http://voices.washingtonpost.com/thefix/eye-on-2008/2008-whale-update.html
BYLINE_TEXT_PATTERN = regex.compile(
    rf'[\n|]{BYLINE_PATTERN}\n', regex.VERBOSE | regex.IGNORECASE
).search

TAGS_SUB = regex.compile(r'</?[a-z][^>]*>', regex.IGNORECASE).sub

# http://www.businessnewsdaily.com/6762-male-female-entrepreneurs.html?cmpid=514642_20140715_27858876
#  .byline > .author
BYLINE_AUTHOR = regex.compile(
    r'<[a-z][^>]*?class=(?<q>["\'])author(?P=q)[^>]*?>(?<result>[^<>]*)',
    regex.IGNORECASE | regex.ASCII
).finditer

STOPWORDS_SEARCH = regex.compile(
    r'''
    \b(?>
        Administrator
        |By
        |Correspondent
        |Editors?
        |News
        |Office
        |People
        |Reporter
        |Staff
        |Writer
        |سایت # tabnak.ir
    )\b
    |\.(?>com|ir)\b
    |www\.
    ''',
    regex.IGNORECASE | regex.VERBOSE,
).search

FOUR_DIGIT_NUM = re_compile('\d\d\d\d').search


def find_authors(html) -> Optional[List[Name]]:
    """Return authors names found in html."""
    names = []
    match_id = None
    for match in META_AUTHOR_FINDITER(html):
        if match_id and match_id != match['id']:
            break
        name = byline_to_names(match['result'])
        if name:
            names.extend(name)
            match_id = match['id']
    if names:
        return names
    match_id = None
    for match in BYLINE_TAG_FINDITER(html):
        # Only match authors using the same search criteria.
        if match_id and match_id != match['id']:
            break
        if match['tag']:
            tag_text = TAGS_SUB('', match['result'])
            ns = byline_to_names(tag_text)
            if ns:
                match_id = match['id']
                names.extend(ns)
                continue
            for m in BYLINE_AUTHOR(match['result']):
                author = m['result']
                ns = byline_to_names(author)
                if ns:
                    names.extend(ns)
            if names:
                return names
        else:
            # not containing tags.
            ns = byline_to_names(match['result'])
            if ns:
                match_id = match['id']
                names.extend(ns)
    if names:
        return names
    match = BYLINE_TEXT_PATTERN(TAGS_SUB('', html))
    if match:
        return byline_to_names(match[0])
    return None


def byline_to_names(byline) -> Optional[List[Name]]:
    r"""Find authors in byline sting. Return name objects as a list.

    The "By " prefix will be omitted.
    Names will be seperated either with " and " or ", ".
    
    If any of the STOPWORDS is found in a name then it will be omitted from
    the result.

    Examples:

    >>> byline_to_names('\n By Roger Highfield, Science Editor \n')
    [RawName("Roger Highfield")]

    >>> byline_to_names(
    ...    ' By Erika Solomon in Beirut and Borzou Daragahi, '
    ...    'Middle East correspondent'
    ... )
    [RawName("Erika Solomon"), RawName("Borzou Daragahi")]
    """
    byline = byline.partition('|')[0]
    if ':' in byline or ':' in byline:
        return None
    m = ANYDATE_SEARCH(byline)
    if m:
        # Removing the date part
        byline = byline[:m.start()]
    if not byline:
        return None
    if FOUR_DIGIT_NUM(byline):
        return None
    # Normalize 'and\n' (and the similar) to standard 'and '
    # This should be done before cutting the byline at the first newline
    byline = NORMALIZE_ANDS(' and ', byline)
    byline = NORMALIZE_COMMA_SPACES(', ', byline)
    # Remove starting "by", cut at the first newline and lstrip
    byline = BY_PREFIX(r'\1', byline)
    # Removing ending " and" or ',' and rstrip
    byline = AND_OR_COMMA_SUFFIX('', byline)
    if ' and ' in byline.lower() or ' ' in byline.partition(', ')[0]:
        fullnames = AND_OR_COMMA_SPLIT(byline)
    else:
        # Comma may be the separator of first name and last name.
        fullnames = AND_SPLIT(byline)
    names = []
    for fullname in fullnames:
        fullname = fullname.partition(' in ')[0].partition(' for ')[0]
        if STOPWORDS_SEARCH(fullname):
            continue
        try:
            name = RawName(fullname)
        except InvalidNameError:
            continue
        lastname = name.lastname
        firstname = name.firstname
        fn_startswith = firstname.startswith
        if (
            fn_startswith('The ')
            or fn_startswith('خبرگزار')
            or lastname.islower()
        ):
            name.nofirst_fulllast()
        names.append(name)
    if not names:
        return None
    # Remove names not having firstname (orgs)
    name0 = names[0]  # In case no name remains at the end
    names = [n for n in names if n.firstname]
    if not names:
        names.append(name0)
    return names