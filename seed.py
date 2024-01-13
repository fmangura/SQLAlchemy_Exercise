from app import app
from models import db, User, Post, Tag

db.drop_all()
db.create_all()

User.query.delete()

def generateSeed():
    Alan = User(first_name='Alan', last_name='Alda')
    Joel = User(first_name='Joel', last_name='Burton')
    Jane = User(first_name='Jane', last_name='Smith')

    db.session.add(Joel)
    db.session.add(Alan)
    db.session.add(Jane)
    db.session.commit()

    ran = Tag(name='random')
    nice = Tag(name='niceThings')

    db.session.add(ran)
    db.session.add(nice)
    db.session.commit()

    Alan_id = User.query.filter(id=='1')
    Joel_id = User.query.filter(id=='2')
    Jane_id = User.query.filter(id=='3')

    Alan_post = Post(title='Alans Post', content='yeahyeah', user_id='1')
    Alan2_post = Post(title='Alans 2nd Post', content='yeahyeahyeah', user_id='1')
    Joel_post = Post(title='Joels Post', content='yeeeedawg', user_id='2')

    db.session.add(Alan_post)
    db.session.add(Alan2_post)
    db.session.add(Joel_post)
    db.session.commit()

    Alan_post.tags.append(ran)
    Alan2_post.tags.append(ran)
    db.session.add(Alan_post)
    db.session.add(Alan2_post)
    db.session.commit()

generateSeed()

