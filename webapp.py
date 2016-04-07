# -*- coding: utf-8 -*-

import time
# import re
# import random
import os
# import getpass

from sys import argv
from uuid import uuid4
# from pymysql import connect
from logging import debug, info, warning, error, exception

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, ErrorHandler, Application, authenticated, asynchronous, StaticFileHandler
from tornado.log import define_logging_options
from tornado import autoreload
from tornado.options import define, options, parse_command_line, parse_config_file

import feedparser
from time import mktime
from datetime import datetime, timedelta

from urllib2 import quote, unquote

def beuDate(rawTime):
    return datetime.fromtimestamp(mktime(rawTime))

class FastFeed(RequestHandler):
    def get(self):
        u = 'http://artgorbunov.ru/news/rss/' # or u = rawdata
        u = self.get_argument('url', None)
        
        if not u:
            self.redirect('/')
            return
        
        r = feedparser.parse(u)
        
        self.render('live.html', feed = r, beuDate = beuDate)
        
        return
        # print r.feed.title
        # i = 0;
        # for item in r.entries:
        #     i+=1
        #     print '\n-=-=-=- %s -=-=-=-' % i
        #     print item.title
        #     # print item.updated # Unicode String
        #     dt = datetime.fromtimestamp(mktime(item.published_parsed))
        #
        #     print dt.strftime('%Y %m %d') # Unicode String
        #     print item.link
            
class Home(RequestHandler):
    def get(self):
        self.render('main.html')


if __name__ == "__main__":
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_PATH = os.path.join(CURRENT_PATH, 'templates')
    STATIC_PATH = os.path.join(CURRENT_PATH, 'static')
    
    define("debug", type=bool, default=False)
    define("templates_path", default=TEMPLATE_PATH)
    define("static_path", default=STATIC_PATH)
    
    # define("db_username", type=str, default="123")
    # define("db_pass", type=str, default="123")
    
    if len(argv) > 1 and os.path.exists(argv[1]):
        parse_config_file(argv[1])
    else:
        warning('Running without config: terminate')
        print('Example usage:')
        print('  python webapp.py /path/to/production.conf [params]')
        exit()
    
    
    urls = [
        ('/', Home),
        (r'/live/', FastFeed),
        (r'/static/(.*)', StaticFileHandler, dict(path=options.static_path))
    ]
    
    settings = dict(
        debug = options.debug,
        template_path = options.templates_path,
        static_path = options.static_path,
        autoescape = None,
        cookie_secret = 'nklfsdkbfhbkewbkbjkwebjkv',
        # db = DBInstance(options.db_username, options.db_pass),
        options = options
    )
    
    http_server = HTTPServer(Application(urls, **settings), xheaders=True)
    http_server.listen(11008)
    
    debug('started http://localhost:11008/')
    
    autoreload.start()
    IOLoop.instance().start()
