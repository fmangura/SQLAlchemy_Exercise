from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = True

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """Tests Users"""

    def setUp(self):
        """Removes existing info"""

        user = User(first_name="First", last_name="Last", image_url="")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Deletes only the this test's user data"""
        user = User.query.filter_by(id=self.user_id).first()
        db.session.delete(user)
        db.session.commit()
        db.session.rollback()

    def test_users_page(self):
        """Tests the homepage"""
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('First', html)

    def test_userInfo(self):
        """Tests accessing the user info"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>First Last</h1>', html)

    def test_addUser(self):
        """Tests creating a user"""
        with app.test_client() as client:
            new = {"first_name": "Neval", "last_name" : "Longbottom", "img": " "}
            resp = client.post('/users/new', data=new, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_editUser(self):
        """Tests editing a user"""
        with app.test_client() as client:
            client.get(f"/users/{self.user_id}/edit")

            new = {"first_name": "nofirst", "last_name" : "nolast", "img": " "}
            resp = client.post(f'/users/{self.user_id}/edit', data=new, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('<h1>First Last</h1>', html)

class PostTestCase(TestCase):
    """Tests Posts"""

    def setUp(self):
        """Removes existing info. creates users and makes a post for the first user."""

        self.user = User(first_name="TestPost", last_name="Test", image_url="")
        self.user2 = User(first_name="Post2", last_name="Test2", image_url="")
        db.session.add(self.user)
        db.session.add(self.user2)
        db.session.commit()
        self.testuser_id = self.user.id

        post = Post(title="Test Title", content="Test Content", user_id=self.testuser_id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

    def tearDown(self):
        """Deletes only this test's data"""
        db.session.rollback()
        Post.query.delete()
        db.session.delete(self.user)
        db.session.delete(self.user2)
        db.session.commit()

    def test_post_page(self):
        """Tests accessing posts"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Title</h1>', html)

    def test_create_post(self):
        """Tests creating posts"""
        with app.test_client() as client:
            client.get(f"/users/{self.testuser_id}/posts/new")
            new = {"title": "createTest", "content" : "testing content"}

            resp = client.post(f"/users/{self.testuser_id}/posts/new", data=new, follow_redirects=True)
            test = Post.query.filter_by(title="createTest").first()

            post = client.get(f'/posts/{test.id}')
            html = post.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(post.status_code, 200)
            self.assertIn('<h1>createTest</h1>', html)
            

    def test_edit_post(self):
        """Tests editing posts"""
        with app.test_client() as client:
            client.get(f"/posts/{self.post_id}/edit")

            new = {"title": "NewTitle", "content" : "NewContent"}
            resp = client.post(f'/posts/{self.post_id}/edit', data=new, follow_redirects=True)
            
            post = client.get(f"/posts/{self.post_id}")
            html = post.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("<h1>Test Title</h1>", html)