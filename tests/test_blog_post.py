# tests/test_blog_post.py

import unittest
from app import create_app  # Ensure this import is correct
from app.models import db

class BlogTestCase(unittest.TestCase):

    def setUp(self):
        # Create the app using the 'testing' configuration
        self.app = create_app('testing')  # Pass the config name
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create the tables in the test database
        db.create_all()

    def tearDown(self):
        # Drop all tables after tests
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Add your test methods here, for example:
    def test_create_blog(self):
        # Test creating a new blog post
        pass

    def test_delete_blog(self):
        # Test deleting a blog post
        pass

    def test_update_blog(self):
        # Test updating a blog post
        pass

if __name__ == '__main__':
    unittest.main()
