import unittest

from gluon.globals import Request
from gluon import current

appname = current.request.application
db = test_db  # Rename the test database so that functions will use it instead of the real database

testFile = "applications/%s/controllers/project.py"%appname
execfile(testFile, globals())

# Clear the database
db.auth_user.truncate()
db.project.truncate()
db.field.truncate()
db.doc.truncate()
db.commit()

# Setup DB

# Setup Test User
db.auth_user.insert(username='testUser', first_name='Test', last_name='User', email='test@example.com', password=db.auth_user.password.validate('P4ssword'))
db.auth_user.insert(username='testUser2', first_name='Test2', last_name='User', email='test2@example.com', password=db.auth_user.password.validate('P4ssword'))
db.commit()
auth.login_bare('testUser','P4ssword')

# Setup Project
db.project.insert(title="IAPT Test Project", manager=1, status=1)
db.commit()
placeholderImage = "applications/%s/static/images/upload/placeholder-project-image.jpg"%appname
stream = open(placeholderImage, 'rb')
db.doc.insert(project=1, name="IAPT Test Doc 1", img=stream)

db.field.insert(project=1, name="Short Field", status=1)
db.field.insert(project=1, name="Long Field", status=2)
db.commit()

db.project.insert(title="IAPT Test Project 2", manager=2, status=1)
db.commit()


# Test Cases
class TestViewOpenWhenClosed(unittest.TestCase):
    def setUp(self):
        request = Request()  # Use a clean Request object

    def testViewOpenWhenClosed(self):
        # Set variables for the test function

        resp = view_open()
        db.commit()
        self.assertEquals(0, len(resp["projects"]))

class TestViewOpenWhenOpen(unittest.TestCase):
    def setUp(self):
        request = Request()  # Use a clean Request object
        db(db.project.id == 1).update(status=2)

    def tearDown(self):
        db(db.project.id == 1).update(status=1)

    def testViewOpenWhenOpen(self):
        # Set variables for the test function

        resp = view_open()
        db.commit()
        self.assertEquals(1, len(resp["projects"]))

class TestViewMine(unittest.TestCase):
    def setUp(self):
        request = Request()

    def testViewMine(self):
        resp = view_mine()
        db.commit()
        self.assertEquals(1, len(resp["projects"]))

# TODO : other test cases

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestViewOpenWhenClosed))
suite.addTest(unittest.makeSuite(TestViewOpenWhenOpen))
#suite.addTest(unittest.makeSuite(TestViewMine))
unittest.TextTestRunner(verbosity=2).run(suite)
