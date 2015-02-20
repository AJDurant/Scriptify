
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

