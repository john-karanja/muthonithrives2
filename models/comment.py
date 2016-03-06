__author__ = 'ISP-PC'

from google.appengine.ext import ndb
from datetime import datetime

class CommentDB(ndb.Model):
    blogid = ndb.StringProperty(default='blogid')
    person = ndb.StringProperty(default='private')
    comment = ndb.StringProperty(default='comment')
    date = ndb.DateTimeProperty(auto_now_add=True)