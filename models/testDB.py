# Create a test database that's laid out just like the "real" database
#
import copy

test_db = DAL('sqlite://testing.sqlite')  # Name and location of the test DB file

for tablename in db.tables:  # Copy tables!
    table_copy = [copy.copy(f) for f in db[tablename]]
    test_db.define_table(tablename, *table_copy)

if test_db(test_db.project_status.id > 0).count() == 0:
    test_db.project_status.insert(name='Closed')
    test_db.project_status.insert(name='Open')

if test_db(test_db.field_type.id > 0).count() == 0:
    test_db.field_type.insert(name='Short Text')
    test_db.field_type.insert(name='Long Text')

if test_db(test_db.contribution_status.id > 0).count() == 0:
    test_db.contribution_status.insert(name='Pending')
    test_db.contribution_status.insert(name='Accepted')
    test_db.contribution_status.insert(name='Rejected')
