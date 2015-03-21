# Create a test database that's laid out just like the "real" database
#
import copy

test_db = DAL('sqlite://testing.sqlite')  # Name and location of the test DB file

for tablename in db.tables:  # Copy tables!
    table_copy = [copy.copy(f) for f in db[tablename]]
    test_db.define_table(tablename, *table_copy)
