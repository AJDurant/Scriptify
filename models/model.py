
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
    Field('owner', 'reference auth_user', writable=False, readable=False, required=True),
    Field('status', 'reference project_status', writable=False, readable=False, required=True),
    format='%(title)s'
)
# Project data constraints
db.project.title.requires = IS_NOT_EMPTY()
db.project.owner.requires = IS_IN_DB(db, db.auth_user.id, '%(username)s')
db.project.status.requires = IS_IN_DB(db, db.project_status.id, '%(name)s')

# Lookup table for field types
db.define_table(
    'field_type',
    Field('name', required=True),
    format='%(name)s'
)

# Table for Project fields
db.define_table(
    'field',
    Field('project', 'reference project', writable=False, readable=False, required=True),
    Field('name', required=True),
    Field('status', 'reference field_type', required=True),
    format='%(project)s: %(name)s'
)
# Field data constraints
db.field.project.requires = IS_IN_DB(db, db.project.id, '%(title)s')
db.field.name.requires = IS_NOT_EMPTY()
db.field.status.requires = IS_IN_DB(db, db.field_type.id, '%(name)s', error_message='You must select a field type')

# Table for Project documents
db.define_table(
    'document',
    Field('project', 'reference project', writable=False, readable=False, required=True),
    Field('name', required=True),
    Field('img',
        'upload',
        label='Document Image',
        autodelete=True,
        uploadseparate=True,
        required=True),
    format='%(name)s'
)
# Document data constraints
db.document.project.requires = IS_IN_DB(db, db.project.id, '%(title)s')
db.document.name.requires = IS_NOT_EMPTY()
db.document.img.requires = IS_IMAGE(extensions=('png', 'jpg', 'jpeg', 'gif'))

# Table for User Contributions
db.define_table(
    'contribution',
    Field('document', 'reference document', writable=False, readable=False, required=True),
    Field('user', 'reference auth_user', writable=False, readable=False, required=True),
    format='%(document)s (%(user)s)'
)

# Lookup table for Contribution Status
db.define_table(
    'contribution_status',
    Field('name', required=True),
    format='%(name)s'
)

# Table for supplied meta-data
db.define_table(
    'metadata',
    Field('contribution', 'reference contribution', writable=False, readable=False, required=True),
    Field('field', 'reference field', writable=False, readable=False, required=True),
    Field('value', 'text', required=True),
    Field('status', 'reference contribution_status', writable=False, readable=False, required=True),
    format='%(field)s - %(contribution)s'
)
db.metadata.contribution.requires = IS_IN_DB(db, db.contribution.id, '%(document)s')
db.metadata.field.requires = IS_IN_DB(db, db.field.id, '%(name)s')
db.metadata.value.requires = IS_NOT_EMPTY()
db.metadata.status.requires = IS_IN_DB(db, db.contribution_status.id, '%(name)s')
