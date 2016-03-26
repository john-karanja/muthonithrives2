#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
from google.appengine.api import mail
from models.blog import BlogDB
from models.blogger import BloggerDB
from models.comment import CommentDB
from models.blog import ImageDB
from models.blog import VideoDB
from google.appengine.api import users



template_path = os.path.join(os.path.dirname(__file__))

jinja2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_path))

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

blog = []
comment = []

class MainHandler(webapp2.RequestHandler):

    def get(self):

        global blog
        global comment
        regblogger = 0
        blog = BlogDB.query(BlogDB.status == 'active').order(-BlogDB.date)
        comment = CommentDB.query().order(-CommentDB.date)
        image = ImageDB.query()


        template_values = {
            'image':image,
            'blog':blog,
            'comment':comment,
            'regblogger':regblogger
        }
        notification = self.request.get('notification')
        if notification:
            template_values['notification'] = notification
        self.response.set_status(200)
        template = jinja2_env.get_template('templates/home.html')
        self.response.out.write(template.render(template_values))



class RegisterHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            regblogger = 0
            template_values = {
                'regblogger':regblogger
            }
            notification = self.request.get('notification')
            if notification:
                template_values['notification'] = notification
            self.response.set_status(200)
            template = jinja2_env.get_template('templates/register.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        user = users.get_current_user()
        if user:
            usermail = user.email()
            firstname = self.request.get('firstname')
            lastname = self.request.get('lastname')
            username = self.request.get('username')
            email = str(usermail)

            blogger = BloggerDB.query().get()
            if blogger > 0:
                privilege = 'user'
                status = 'suspended'
            else:
                privilege = 'admin'
                status = 'active'


            check1 = BloggerDB.query(BloggerDB.email == email).get()
            check2 = BloggerDB.query(BloggerDB.username == username).get()

            if check1 > 0 or check2 > 0:
                self.redirect('/register?notification=blogger account exists')
            else:

                blogger = BloggerDB(
                    fname = str(firstname),
                    lname = str(lastname),
                    username = str(username),
                    email = str(email),
                    status = str(status),
                    privilege = str(privilege)
                )

                blogger.put()

                self.redirect('/register')
        else:
            self.redirect(users.create_login_url(self.request.uri))

class AboutHandler(webapp2.RequestHandler):

    def get(self):
        global blog
        global comment
        regblogger = 0
        blog = BlogDB.query(BlogDB.status == 'active').order(-BlogDB.date)
        comment = CommentDB.query().order(-CommentDB.date)
        image = ImageDB.query()


        template_values = {
            'image':image,
            'blog':blog,
            'comment':comment,
            'regblogger':regblogger
        }
        notification = self.request.get('notification')
        if notification:
            template_values['notification'] = notification
        self.response.set_status(200)
        template = jinja2_env.get_template('templates/about.html')
        self.response.out.write(template.render(template_values))



class BlogHandler(webapp2.RequestHandler):

    def get(self):

        global blog
        global comment
        global blogsl

        regblogger = 0
        blog = BlogDB.query(BlogDB.status == 'active')
        bl = blog.get()

        title = self.request.get('title',bl.title)
        comment = []

        video = VideoDB.query()
        image = ImageDB.query()

        blogsl = BlogDB.query(BlogDB.status == 'active',BlogDB.title == title).get()
        slid = str(blogsl.key.id())
        if blogsl:
            comment = CommentDB.query(CommentDB.blogid == slid)

        template_values = {
            'regblogger':regblogger,
            'video':video,
            'image':image,
            'blog':blog,
            'blogsl':blogsl,
            'comment':comment
        }
        notification = self.request.get('notification')
        if notification:
            template_values['notification'] = notification
        self.response.set_status(200)
        template = jinja2_env.get_template('templates/myblog.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        global blogsl
        blogid = self.request.get('blogid')
        person = self.request.get('person')
        comment = self.request.get('comment')

        comment = CommentDB(
            blogid = str(blogid),
            person = str(person),
            comment = str(comment)
        )

        comment.put()

        self.redirect('/blog')


class NewHandler(webapp2.RequestHandler):

    def get(self):

        if users.get_current_user():
            usermail = users.get_current_user().email()
            thisuser = BloggerDB.query(BloggerDB.email==usermail,BloggerDB.status=='active').get()

            global blog
            global comment

            if thisuser:
                blogger = thisuser.username
                regblogger = 1
                template_values = {

                    'regblogger':regblogger,
                    'blogger':blogger

                }
                notification = self.request.get('notification')
                if notification:
                    template_values['notification'] = notification
                self.response.set_status(200)
                template = jinja2_env.get_template('templates/new.html')
                self.response.out.write(template.render(template_values))
            else:
                self.redirect('/')

        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):

        if users.get_current_user():

            usermail = users.get_current_user().email()
            thisuser = BloggerDB.query(BloggerDB.email==usermail,BloggerDB.status=='active').get()

            if thisuser:
                null = 'null'

                title = str(self.request.get('title',null))
                image = str(self.request.get('image',null))
                content = self.request.get('content',null)
                blogger_ = thisuser.username

                if title == "":
                    title = str(null)
                if content == "":
                    content = str(null)

                newblog = BlogDB(
                    blogger = blogger_,
                    title = title,
                    image = image,
                    content = content,

                )
                newblog.put()

                self.redirect('/new')

            self.redirect('/')

        else:
            self.redirect(users.create_login_url(self.request.uri))

class EditHandler(webapp2.RequestHandler):

    def get(self):

        if users.get_current_user():

            usermail = users.get_current_user().email()
            thisuser = BloggerDB.query(BloggerDB.email==usermail,BloggerDB.status=='active').get()

            if thisuser:

                global blog
                global comment
                blogedit = []
                myblogs2edit = []
                regblogger = 1

                id = self.request.get('id')
                myblog = BlogDB.query(BlogDB.blogger == thisuser.username)

                for b in myblog:
                    myblogs2edit.append(b)

                if id !="":
                    be = BlogDB.get_by_id(int(id))
                    blogedit.append(be)

                template_values = {
                    'regblogger':regblogger,
                    'blogs2edit':myblogs2edit,
                    'blogedit':blogedit
                }
                notification = self.request.get('notification')
                if notification:
                    template_values['notification'] = notification
                self.response.set_status(200)
                template = jinja2_env.get_template('templates/edit.html')
                self.response.out.write(template.render(template_values))
            else:
                self.redirect('/')

        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):

        if users.get_current_user():
            usermail = users.get_current_user().email()
            thisuser = BloggerDB.query(BloggerDB.email==usermail,BloggerDB.status=='active').get()

            if thisuser:

                title = self.request.get('title')
                image = self.request.get('image')
                content = self.request.get('content')
                id = self.request.get('id')

                blog = BlogDB.get_by_id(int(id))

                blog.title = title
                blog.image = image
                blog.content = content
                blog.put()

                self.redirect('/edit')
            else:
                self.redirect('/')

        else:
            self.redirect(users.create_login_url(self.request.uri))

class BloggerHandler(webapp2.RequestHandler):

    def get(self):
        if users.get_current_user():

            global blog
            global comment

            regblogger = 1
            usermail = users.get_current_user().email()
            thisuser = BloggerDB.query(BloggerDB.email==usermail,BloggerDB.privilege=='admin').get()

            if thisuser:

                blogger = BloggerDB.query()

                template_values = {

                    'blogger':blogger,
                    'regblogger':regblogger,
                }
                notification = self.request.get('notification')
                if notification:
                    template_values['notification'] = notification
                self.response.set_status(200)
                template = jinja2_env.get_template('templates/blogger.html')
                self.response.out.write(template.render(template_values))
            else:
                self.redirect('/')

        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        user = users.get_current_user()
        if user:

            usermail = users.get_current_user().email()
            new = self.request.get('new')
            activate = self.request.get('activate')
            suspend = self.request.get('suspend')
            error = self.request.get('error')
            blogger_ = BloggerDB.query()

            thisuser = BloggerDB.query(BloggerDB.email==usermail,BloggerDB.privilege=='admin').get()

            if thisuser >0:

                if new !='':

                        fname = self.request.get('fname')
                        lname = self.request.get('lname')
                        email = self.request.get('email')
                        username = self.request.get('username')
                        privilege = self.request.get('privilege')

                        check1 = BloggerDB.query(BloggerDB.email == email).get()
                        check2 = BloggerDB.query(BloggerDB.username == username).get()

                        if check1 > 0 or check2 > 0:
                            self.redirect('/blogger?notification=blogger account exists')
                        else:
                            newblogger = BloggerDB(
                                fname = str(fname),
                                lname = str(lname),
                                username = str(username),
                                email = str(email),
                                privilege = str(privilege)
                            )
                            newblogger.put()

                        self.redirect('/blogger')
                else:
                        self.redirect('/blogger')

                if activate != '':
                        for b in blogger_:
                            if b.email == activate:
                                b.status = 'active'
                                b.put()

                if suspend != '':
                        for b in blogger_:
                            if b.email == suspend:
                                b.status = 'suspended'
                                b.put()

                if error != '':
                        for b in blogger_:
                            if b.email == error:
                                b.status = 'deactive'
                                b.put()

                self.redirect('/blogger')

            else:
                self.redirect('/blogger')


        else:
                self.redirect(users.create_login_url(self.request.uri))

class BlogsHandler(webapp2.RequestHandler):

    def get(self):
        global blog
        global comment

        user = users.get_current_user()
        if user :
            usermail = user.email()
            thisuser = BloggerDB.query(BloggerDB.email==usermail,BloggerDB.status == 'active').get()

            if thisuser > 0 :
                regblogger = 1
                if thisuser.privilege == 'admin':
                    blogset = BlogDB.query()
                elif thisuser.privilege == 'user':
                    blogset = BlogDB.query(BlogDB.blogger == thisuser.username)
                else:
                    blogset = []

                template_values = {

                    'blogset':blogset,
                    'regblogger':regblogger,
                }
                notification = self.request.get('notification')
                if notification:
                    template_values['notification'] = notification
                self.response.set_status(200)
                template = jinja2_env.get_template('templates/blogs.html')
                self.response.out.write(template.render(template_values))
            else:
                self.redirect('/')

        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        if users.get_current_user():
            publish = self.request.get('publish')
            deactivate = self.request.get('deactivate')
            error = self.request.get('error')

            blog_ = BlogDB.query()

            if publish != '':
                for b in blog_:
                    if b.title == publish:
                        b.status = 'active'
                        b.put()

            if deactivate != '':
                for b in blog_:
                    if b.title == deactivate:
                        b.status = 'deactive'
                        b.put()

            if error != '':
                for b in blog_:
                    if b.title == error:
                        b.status = 'deactive'
                        b.put()

            self.redirect('/blogs')

        else:
            self.redirect(users.create_login_url(self.request.uri))

class GalleryHandler(webapp2.RequestHandler):

    def get(self):
        blog = []

        user = users.get_current_user()
        if user :
            usermail = user.email()
            thisuser = BloggerDB.query(BloggerDB.email==usermail,BloggerDB.status == 'active').get()
            if thisuser > 0:
                regblogger = 1
                blog = BlogDB.query(BlogDB.blogger == thisuser.username)
                image = ImageDB.query()
                video = VideoDB.query()

                template_values = {
                    'regblogger':regblogger,
                    'blog':blog,
                    'image':image,
                    'video':video
                }
                notification = self.request.get('notification')
                if notification:
                    template_values['notification'] = notification
                self.response.set_status(200)
                template = jinja2_env.get_template('templates/gallery.html')
                self.response.out.write(template.render(template_values))
            else:
                self.redirect('/')

        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):

        user = users.get_current_user()
        newimg = self.request.get('newimg')
        newvideo = self.request.get('newvideo')
        name = self.request.get('name')
        link = self.request.get('link')
        blog = self.request.get('blog')
        block = self.request.get('block')
        if user :
            usermail = user.email()
            thisuser = BloggerDB.query(BloggerDB.email==usermail,BloggerDB.status == 'active').get()
            if thisuser:
                if newimg == '1':
                    image = ImageDB(
                        name = str(name),
                        link = str(link),
                        blog = str(blog),
                        block = str(block)
                    )
                    image.put()
                if newvideo == '1':
                    video = VideoDB(
                        name = str(name),
                        link = str(link),
                        blog = str(blog),
                        block = str(block)
                    )
                    video.put()
                self.redirect('/gallery')
        else:
             self.redirect('/')


class Try(webapp2.RequestHandler):

    def get(self):
        comment= []


        blog = BlogDB_.query().get()
        template_values = {
            'blog':blog,
            'comment':comment
        }
        notification = self.request.get('notification')
        if notification:
            template_values['notification'] = notification
        self.response.set_status(200)
        template = jinja2_env.get_template('templates/blog_.html')
        self.response.out.write(template.render(template_values))

class LogOut(webapp2.RequestHandler):
    def get(self):

            user = users.get_current_user()
            if user:
                sign = ('Click to sign out, %s! (<a href="%s">sign out</a>)' %
                            (user.nickname(), users.create_logout_url('/')))
            else:
                sign = ('<a href="%s">Sign in </a>.' %
                            users.create_login_url('/'))

            self.response.out.write("<html><body>%s</body></html>" % sign)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/new', NewHandler),
    ('/edit', EditHandler),
    ('/blogger', BloggerHandler),
    ('/blog', BlogHandler),
    ('/blogs', BlogsHandler),
    ('/logout',LogOut),
    ('/gallery',GalleryHandler),
    ('/register',RegisterHandler),
    ('/try' , Try),
    ('/about', AboutHandler),
], debug=True)
