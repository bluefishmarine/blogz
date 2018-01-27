from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship("Comment", backref="blog")

    def __init__(self, title, body, user, pub_date=None):
        self.title = title
        self.body = body
        self.owner = user
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref="owner")
    comments = db.relationship("Comment", backref="owner")

    def __init__(self,email,password):
        self.email = email
        self.password = password

class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id')) 

    def __init__(self,content,user,blog,pub_date=None):
        self.content = content
        self.owner = user
        self.blog = blog
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
