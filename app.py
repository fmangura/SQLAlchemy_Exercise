"""Blogly application."""
from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
import psycopg2 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "bloglySQLAlchemy"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()

# db.drop_all()
# db.create_all()


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
    """Create new user"""
    first = request.form['first_name']
    last = request.form['last_name']
    image = request.form['img']

    user = User(first_name=first, last_name=last, image_url=image)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_ids>')
def show_user(user_ids):
    """Show user info"""

    user = User.query.get_or_404(user_ids)
    posts = Post.query.filter(Post.user_id == user_ids).all()
    return render_template("userinfo.html", user=user, posts=posts)

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

@app.route('/users/<int:user_id>/posts/new')
def make_post(user_id):
    """Show Post Form"""
    user = User.query.get_or_404(user_id)
    return render_template('postform.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_post(user_id):
    """Posts post"""
    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect("/users")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Shows Post"""
    post = Post.query.get_or_404(post_id)
    return render_template('postdetails.html', post=post)

@app.route('/posts/<int:post_id>/delete')
def del_post(post_id):
    """delete post"""

    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show Post Edit Form"""
    post = Post.query.get_or_404(post_id)
    return render_template('postedit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def post_edit_post(post_id):
    """Confirm Edit post"""
    title = request.form['title']
    content = request.form['content']

    post = Post.query.filter_by(id=post_id).first()
    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    return redirect("/")

