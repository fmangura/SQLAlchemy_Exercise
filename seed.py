from app import app
from models import db, User

db.drop_all()
db.create_all()

User.query.delete()

Alan = User(first_name='Alan', last_name='Alda')
Joel = User(first_name='Joel', last_name='Burton')
Jane = User(first_name='Jane', last_name='Smith')

db.session.add(Alan)
db.session.add(Joel)
db.session.add(Jane)
db.session.commit()