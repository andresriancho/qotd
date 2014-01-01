# -*- coding: utf-8 -*-

#    Copyright (C) 2010 Yuen Ho Wong
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import with_statement

import re
import os
import random
import copy
import time
from BaseHTTPServer import BaseHTTPRequestHandler
from datetime import datetime, date
from urllib2 import urlopen, URLError
from cPickle import dump, load, HIGHEST_PROTOCOL
from xml.sax import make_parser, SAXException
from xml.sax.handler import ContentHandler, property_xml_string

DOT_FILE_PATH = os.path.join(os.path.expanduser("~"), ".qotd")


class Quote(object):
    def __init__(self, author=None, content=None, pubDate=None, printed=False):
        self.author = author
        self.content = content
        self.pubDate = pubDate
        self.printed = printed

    def __cmp__(self, other):
        if self.pubDate < other.pubDate:
            return -1
        elif self.pubDate == other.pubDate:
            return 0
        elif self.pubDate > other.pubDate:
            return 1

    def __str__(self):
        # Replace the Unicode replacement character often found in the RSS feed
        # with a space and then encode the Unicode string to a UTF8 byte string
        # as per the __str__ protocol demands.
        return ((self.content or u'') + u'\n-- ' + (self.author or u'')).replace(u'\ufffd', u' ').encode('utf8')


class QOTDFeedHandler(ContentHandler):
    def __init__(self):
        self.quotes = []
        self.quote = None
        self.in_item = False
        self.in_title = False
        self.in_description = False
        self.in_pubDate = False
        self.lexing_tag = False
        self.in_tag = False
        # Hack to recover from a few unrecognized
        # unicode chars bombing out the whole script
        self.has_valid_content = False

    def startElement(self, name, attrs):
        if name == 'item':
            self.in_item = True
            self.quote = Quote()
        elif name == 'title' and self.in_item:
            self.in_title = True
        elif name == 'description' and self.in_item:
            self.in_description = True
        elif name == 'pubDate' and self.in_item:
            self.in_pubDate = True

    def characters(self, content):
        if self.in_item:
            if self.in_title:
                self.quote.author = content
            elif self.in_pubDate:
                st_time = time.strptime(content, u"%a, %d %b %Y %H:%M:%S %Z")
                self.quote.pubDate = date.fromtimestamp(time.mktime(st_time))
            elif self.in_description:
                if content == '<':
                    self.lexing_tag = True
                elif content == '>':
                    self.lexing_tag = False
                elif content.isspace():
                    return
                elif content.startswith('/'):
                    if self.lexing_tag:
                        self.in_tag = False
                    else:
                        self.in_tag = True
                else:
                    if self.in_tag:
                        return
                    elif not self.lexing_tag and not self.in_tag:
                        l = re.findall(ur'".+"', content)
                        if l:
                            self.quote.content = l[0]
                            self.has_valid_content = True

    def endElement(self, name):
        if name == 'item':
            self.in_item = False
            if self.has_valid_content:
                self.quotes.append(self.quote)
                self.has_valid_content = False
        elif name == 'title' and self.in_item:
            self.in_title = False
        elif name == 'description' and self.in_item:
            self.in_description = False
        elif name == 'pubDate' and self.in_item:
            self.in_pubDate = False


def update_quotes_cache():
    quotes = None
    resp = urlopen("http://www.quotationspage.com/data/qotd.rss")
    parser = make_parser()
    handler = QOTDFeedHandler()
    parser.setContentHandler(handler)
    try:
        parser.parse(resp)
    except SAXException, e:
        print 'Error parsing qotd.rss', e
        pass
    else:
        quotes = copy.deepcopy(handler.quotes)
        resp = urlopen('http://www.quotationspage.com/data/mqotd.rss')
        parser = make_parser()
        handler = QOTDFeedHandler()
        parser.setContentHandler(handler)
        try:
            parser.parse(resp)
        except SAXException, e:
            print 'Error parsng mqotd.rss', e
            pass
        quotes += handler.quotes
        # Cache the quotes for a day
        with open(DOT_FILE_PATH, 'w') as dotfile:
            dump(quotes, dotfile, HIGHEST_PROTOCOL)
    return quotes


def main():
    dotfilestatinfo = None
    try:
        dotfilestatinfo = os.stat(DOT_FILE_PATH)
    except (IOError, OSError):
        try:
            print random.choice(update_quotes_cache())
            return 0
        except URLError, e:
            if hasattr(e, 'code'):
                print 'QuoteOfTheDay: Error %d: %s' % (e.code, BaseHTTPRequestHandler.responses[e.code][1])
            elif hasattr(e, 'reason'):
                print 'QuoteOfTheDay: IO or URL Error: ' + str(e.reason)
            return 1

    lastmod = datetime.fromtimestamp(dotfilestatinfo.st_mtime)

    if (datetime.now() - lastmod).days < 1:
        with open(DOT_FILE_PATH) as dotfile:
            print random.choice(load(dotfile))
    else:
        try:
            print random.choice(update_quotes_cache())
        except URLError, e:
            if hasattr(e, 'code'):
                print 'QuoteOfTheDay: Error %d: %s' % (e.code, BaseHTTPRequestHandler.responses[e.code][1])
            elif hasattr(e, 'reason'):
                print 'QuoteOfTheDay: IO or URL Error: ' + str(e.reason)
            return 1

    return 0
