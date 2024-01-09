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
        return f"<User id={p.id} name={p.first_name}{p.last_name} img={p.image_url}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False, unique=True)

    last_name = db.Column(db.String(50), nullable=False, unique=True)

    image_url = db.Column(db.VARCHAR(2083), default="No Data")

    user_post = db.relationship('Post', backref='User')

class Post(db.Model):
    """User Post Model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(50), nullable=False)

    content = db.Column(db.String(100), nullable=False)

    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), default="1", nullable=False )




