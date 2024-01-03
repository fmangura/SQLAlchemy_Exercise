from flask_sqlalchemy import SQLAlchemy

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



