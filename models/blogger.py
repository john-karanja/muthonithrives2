__author__ = 'ISP-PC'

from google.appengine.ext import ndb
from datetime import datetime

class BloggerDB(ndb.Model):
    email = ndb.StringProperty(default='blogger@muthonithrives.com')
    fname = ndb.StringProperty(default='blogger')
    lname = ndb.StringProperty(default='blogger')
    date = ndb.DateProperty(auto_now_add=True)
    username = ndb.StringProperty(default='null')
    privilege = ndb.StringProperty(default='user')
    status = ndb.StringProperty(default='active')