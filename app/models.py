from app import db
from datetime import datetime
import re
from flask_security import UserMixin, RoleMixin

def makeslug(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


articles_themes = db.Table('articles_themes',
                    db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
                    db.Column('themes_id', db.Integer, db.ForeignKey('themes.id'))
                )


class Articles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), unique=True)
    slug = db.Column(db.String(255), unique=True)
    subtitle = db.Column(db.String(255))
    first_chapter = db.Column(db.Text)
    first_image = db.Column(db.String(255))
    second_chapter = db.Column(db.Text)
    video = db.Column(db.String(255))
    third_chapter = db.Column(db.Text)
    third_image = db.Column(db.String(255))
    conclusion = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())

    comments = db.relationship('Commentaries', backref='articles')

    themes = db.relationship('Themes', secondary=articles_themes, backref=db.backref('articles', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Articles, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = makeslug(self.title)

    def __repr__(self):
        return '<{}>'.format(self.title)


class Themes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(255), unique=True)

    def __init__(self, *args, **kwargs):
        super(Themes, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = makeslug(self.name)

    def __repr__(self):
        return '{}'.format(self.name)


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    comments = db.relationship('Commentaries', backref='user')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))

class Commentaries(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    article_name = db.Column(db.String(255), db.ForeignKey('articles.title'))
    user_name = db.Column(db.String(100), db.ForeignKey('user.name'))
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=datetime.now())




