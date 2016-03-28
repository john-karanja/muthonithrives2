__author__ = 'ISP-PC'

from google.appengine.ext import ndb
from datetime import datetime

class BlogDB(ndb.Model):
    blogger = ndb.StringProperty(default='private')
    title = ndb.StringProperty(default='New blog')
    image = ndb.StringProperty()
    content = ndb.TextProperty(default='null')
    status = ndb.StringProperty(default='active')
    date = ndb.DateTimeProperty(auto_now_add=True)
    slug = ndb.StringProperty()


class newsletterDB(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    status = ndb.StringProperty(default='subscribed')
    date = ndb.DateTimeProperty(auto_now_add=True)


class VideoDB(ndb.Model):
    name = ndb.StringProperty(default='name')
    link = ndb.StringProperty(default='link')
    block = ndb.StringProperty(default='block0')
    blog = ndb.StringProperty(default='none')

class ImageDB(ndb.Model):
    name = ndb.StringProperty(default='name')
    link = ndb.StringProperty(default='link')
    block = ndb.StringProperty(default='block0')
    blog = ndb.StringProperty(default='none')
