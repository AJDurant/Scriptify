import unittest

from gluon.globals import Request
from gluon import current

appname= current.request.application
db = test_db  # Rename the test database so that functions will use it instead of the real database

testFile = "applications/%s/controllers/project.py"%appname
execfile(testFile, globals())

# Clear the database
db.project.truncate()
db.field.truncate()
db.doc.truncate()
db.commit()

# Setup DB

# TODO : Setup Test User

db.project.insert(title="IAPT Test Project", manager=1, status=1)

stream = open("applications/%s/static/images/upload/placeholder-project-image.jpg"%appname, 'rb')
db.doc.insert(project=1, name="IAPT Test Doc 1", img=stream)

db.field.insert(project=1, name="Short Field", status=1)
db.field.insert(project=1, name="Long Field", status=2)

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

    def testViewOpenWhenOpen(self):
        # Set variables for the test function

        resp = view_open()
        db.commit()
        self.assertEquals(1, len(resp["projects"]))

# TODO : other test cases

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestViewOpenWhenClosed))
unittest.TextTestRunner(verbosity=2).run(suite)
