
# DB Table for Users in db.py for auth

# Lookup table for project status
db.define_table(
    'project_status',
    Field('name', required=True),
    format='%(name)s'
)

# DB Table for Projects
db.define_table(
    'project',
    Field('title', required=True, label='Project Title'),
    Field('manager', 'reference auth_user', writable=False, readable=False, required=True),
    Field('status', 'reference project_status', writable=False, readable=False, required=True),
    format='%(title)s'
)
# Project data constraints
db.project.title.requires = IS_NOT_EMPTY()
db.project.manager.requires = IS_IN_DB(db, db.auth_user.id, '%(username)s')
db.project.status.requires = IS_IN_DB(db, db.project_status.id, '%(name)s')

# Get the documents for this project
db.project.documents = Field.Virtual(
    'documents',
    lambda row: db(db.doc.project==row.project.id).select())

# Lookup table for field types
db.define_table(
    'field_type',
    Field('name', required=True),
    Field('fname', required=True),
    format='%(name)s'
)

# Table for Project fields
db.define_table(
    'field',
    Field('project', 'reference project', writable=False, readable=False, required=True),
    Field('name', required=True, label='Field Name'),
    Field('status', 'reference field_type', required=True, label='Field Type'),
    format='%(project)s: %(name)s'
)
# Field data constraints
db.field.project.requires = IS_IN_DB(db, db.project.id, '%(title)s')
db.field.name.requires = IS_NOT_EMPTY()
db.field.status.requires = IS_IN_DB(db, db.field_type.id, '%(name)s', error_message='You must select a field type')

# Table for Project documents
db.define_table(
    'doc',
    Field('project', 'reference project', writable=False, readable=False, required=True),
    Field('name', required=True, label='Document Name'),
    Field('img',
        'upload',
        label='Document Image',
        autodelete=True,
        uploadseparate=True,
        required=True),
    format='%(name)s'
)
# Document data constraints
db.doc.project.requires = IS_IN_DB(db, db.project.id, '%(title)s')
db.doc.name.requires = IS_NOT_EMPTY()
db.doc.img.requires = IS_IMAGE(extensions=('png', 'jpg', 'jpeg', 'gif'))

db.doc.active = Field.Virtual(
    'active',
    lambda row: (
        (db.executesql('SELECT count(metadata.id) FROM metadata, contribution WHERE metadata.contribution = contribution.id AND metadata.status = 2 AND contribution.doc = %(doc)s;' % {'doc': row.doc.id})[0][0] < db.executesql('SELECT count(DISTINCT field.id) FROM field, metadata, contribution WHERE field.id = metadata.field AND metadata.contribution = contribution.id AND contribution.doc = %(doc)s;' % {'doc': row.doc.id})[0][0])
        & (db.executesql('SELECT count(DISTINCT contribution.id) FROM metadata, contribution WHERE metadata.contribution = contribution.id AND metadata.status = 1 AND contribution.doc = %(doc)s;' % {'doc': row.doc.id})[0][0] < 3)
        | (db.executesql('SELECT count(DISTINCT field.id) FROM field, metadata, contribution WHERE field.id = metadata.field AND metadata.contribution = contribution.id AND contribution.doc = %(doc)s AND field.id NOT IN (SELECT field.id FROM field, metadata, contribution WHERE field.id = metadata.field AND metadata.contribution = contribution.id AND contribution.doc = %(doc)s AND (metadata.status = 2 OR metadata.status = 1) GROUP BY field.id);' % {'doc': row.doc.id})[0][0] > 0)
    )
)

# Table for User Contributions
db.define_table(
    'contribution',
    Field('doc', 'reference doc', writable=False, readable=False, required=True),
    Field('contributor', 'reference auth_user', writable=False, readable=False, required=True),
    format='%(doc)s (%(contributor)s)'
)

# Lookup table for Contribution Status
db.define_table(
    'contribution_status',
    Field('name', required=True),
    format='%(name)s'
)

# Table for supplied metadata
db.define_table(
    'metadata',
    Field('contribution', 'reference contribution', writable=False, readable=False, required=True),
    Field('field', 'reference field', writable=False, readable=False, required=True),
    Field('data_value', 'text', required=True),
    Field('status', 'reference contribution_status', writable=False, readable=False, required=True),
    format='%(field)s - %(contribution)s'
)
# Metadata constraints
db.metadata.contribution.requires = IS_IN_DB(db, db.contribution.id, '%(doc)s')
db.metadata.field.requires = IS_IN_DB(db, db.field.id, '%(name)s')
db.metadata.data_value.requires = IS_NOT_EMPTY()
db.metadata.status.requires = IS_IN_DB(db, db.contribution_status.id, '%(name)s')

# Lookup values (added on first run)
if db(db.project_status.id > 0).count() == 0:
    db.project_status.insert(name='Closed')
    db.project_status.insert(name='Open')

if db(db.field_type.id > 0).count() == 0:
    db.field_type.insert(name='Short Text', fname='string')
    db.field_type.insert(name='Long Text', fname='text')

if db(db.contribution_status.id > 0).count() == 0:
    db.contribution_status.insert(name='Pending')
    db.contribution_status.insert(name='Accepted')
    db.contribution_status.insert(name='Rejected')
