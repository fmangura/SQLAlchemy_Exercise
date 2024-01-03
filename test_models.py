from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = True

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """Tests Users"""

    def setUp(self):
        """Removes existing info"""
        User.query.delete()

        user = User(first_name="First", last_name="Last", image_url="")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()

    def test_users_page(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('First', html)

    def test_userInfo(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>First Last</h1>', html)

    def test_addUser(self):
        with app.test_client() as client:
            new = {"first_name": "Neval", "last_name" : "Longbottom", "img": " "}
            resp = client.post('/users/new', data=new, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_editUser(self):
        with app.test_client() as client:
            client.get(f"/users/{self.user_id}/edit")


            new = {"first_name": "nofirst", "last_name" : "nolast", "img": " "}
            resp = client.post(f'/users/{self.user_id}/edit', data=new, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('<h1>First Last</h1>', html)

    
    # def test_redirect(self):
    #     with app.test_client() as client:
    #         resp = client.get('/')

    #         self.assertEqual(resp.status_code, 302)
    #         self.assertEqual(resp.location,"http://localhost/")

    # def test_redication(self):
    #     with app.test_client() as client:
    #         resp = client.get('/', follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('<h1>Users</h1>', html)

