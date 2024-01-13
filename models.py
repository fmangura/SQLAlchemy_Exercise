from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
    """User Model"""

    __tablename__ = "users"

    def __repr__(self):
        p = self
        return f"<User id={p.id} name={p.first_name}{p.last_name} img={p.image_url}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False, unique=True)

    last_name = db.Column(db.String(50), nullable=False, unique=True)

    image_url = db.Column(db.VARCHAR(2083), default="No Data")

    user_post = db.relationship('Post', backref='User')

class Post(db.Model):
    """User Post Model"""

    __tablename__ = "posts"

    def __repr__(self):
        p = self
        return f"<{p.id}, {p.title}, {p.content}, {p.user_id}, {p.created_date}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(50), nullable=False)

    content = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), default="1", nullable=False )

    created_date = db.Column(db.String(200), default=datetime.now(tz=None).strftime("%a %b %d %Y, %I:%M %p"))

    tags = db.relationship('Tag', secondary='post_tags', backref='posts')

class Tag(db.Model):
    """Posts Tags"""

    __tablename__="tags"

    def __repr__(self):
        return f"Tag {self.name}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(50), nullable=False, unique=True)

class PostTag(db.Model):
    """Combined table for both post and tag id"""

    __tablename__= "post_tags"

    def __repr__(self):
        return f"Post:{self.post_id}, Tag:{self.tag_id}"
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)



