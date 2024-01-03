"""Blogly application."""
from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
import psycopg2 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "bloglySQLAlchemy"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
db.create_all()

@app.route('/')
def home():
    """Go to users"""
    return redirect('/users')

@app.route('/users')
def list_users():
    """Lists all users first and last name"""
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/users/new')
def form_New_user():
    """open user form"""
    return render_template("createuser.html")

@app.route('/users/new', methods=["POST"])
def New_user():
    first = request.form['first_name']
    last = request.form['last_name']
    image = request.form['img']

    user = User(first_name=first, last_name=last, image_url=image)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show user info"""

    user = User.query.get_or_404(user_id)
    return render_template("userinfo.html", user=user)

@app.route('/users/<int:user_id>', methods=['POST'])
def del_user(user_id):
    """delete user"""

    currUser = User.query.filter_by(id=user_id).first()
    db.session.delete(currUser)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/edit', methods=["GET"])
def edit_user_form(user_id):
    """Edit user info"""
    user = User.query.get_or_404(user_id)
    return render_template("edituser.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    first = request.form['first_name']
    last = request.form['last_name']
    image = request.form['img']

    currUser = User.query.filter_by(id=user_id).first()
    currUser.first_name = first
    currUser.last_name = last
    currUser.image_url = image

    db.session.add(currUser)
    db.session.commit()

    return redirect("/users")
