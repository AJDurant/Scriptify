"""
This is the project controller
 - create & add_doc & add_field
 - open / close projects
 - view individual/open/my projects

"""

def index():
    """
    Display all projects which are open for croudsourcing

    """
    projects = db(db.project.status == 2).select() # Select projects that are open for croudsourcing
    response.title = "Projects open for contributions"
    return dict(projects=projects)

def view():
    """
    Allow users to view a project
    Show all documents in project
    Link users to contribute to a document

    """
    # Get project or redirect
    try:
        project = db.project(request.args(0,cast=int))
        if project is None:
            raise LookupError
    except:
        redirect(URL('project', 'index'))

    # Get project documents
    documents = db(db.doc.project == project.id).select()

    for doc in documents:
        # Making this a virtual field doesn't seem to work, so it is duplicated =(
        doc.active = (
            (db.executesql('SELECT count(metadata.id) FROM metadata, contribution WHERE metadata.contribution = contribution.id AND metadata.status = 2 AND contribution.doc = %(doc)s;' % {'doc': doc.id})[0][0] < db.executesql('SELECT count(DISTINCT field.id) FROM field, metadata, contribution WHERE field.id = metadata.field AND metadata.contribution = contribution.id AND contribution.doc = %(doc)s;' % {'doc': doc.id})[0][0])
            & (db.executesql('SELECT count(DISTINCT contribution.id) FROM metadata, contribution WHERE metadata.contribution = contribution.id AND metadata.status = 1 AND contribution.doc = %(doc)s;' % {'doc': doc.id})[0][0] < 3)
            | (db.executesql('SELECT count(DISTINCT field.id) FROM field, metadata, contribution WHERE field.id = metadata.field AND metadata.contribution = contribution.id AND contribution.doc = %(doc)s AND field.id NOT IN (SELECT field.id FROM field, metadata, contribution WHERE field.id = metadata.field AND metadata.contribution = contribution.id AND contribution.doc = %(doc)s AND (metadata.status = 2 OR metadata.status = 1) GROUP BY field.id);' % {'doc': doc.id})[0][0] > 0)
        )

    response.title = project.title
    response.subtitle = 'Project Documents'
    return dict(project=project, documents=documents)

@auth.requires_login()
def view_mine():
    """
    Allow users to view all projects that they created

    """
    # Get users projects
    projects = db(db.project.manager == auth.user_id).select()

    response.title = "Projects you created"
    return dict(projects=projects)

@auth.requires_login()
def create():
    """
    Allow users to create projects
    Include form
    - Project Details
    - Documents
    - Fields

    """
    response.title = "Create a new project"

    # Construct form for project creation
    form = SQLFORM(db.project,
        submit_button='Save and Add Fields',
        formstyle='bootstrap3_inline')

    # Assign manager to the current user
    form.vars.manager = auth.user_id
    form.vars.status = 1 # Project status - closed.

    if form.process().accepted:
        session.flash = 'Project Saved'
        redirect(URL('add_field', args=form.vars.id))

    return dict(form=form)

@auth.requires_login()
def add_field():
    """
    Allow users to add fields to a project
    There are two paths
     - loop back to save the field and add another
     - move forward to add documents

    """
    # Get project or redirect
    try:
        project = db.project(request.args(0,cast=int))
        if project is None:
            raise LookupError
    except:
        redirect(URL('project', 'create'))

    response.title = project.title
    response.subtitle = "Add Field"

    # Construct form for project fields - buttons to save the field and to move onward in the form
    form = SQLFORM(
        db.field,
        buttons = [
            TAG.button('Save Field', _class="btn btn-primary", _type="submit"),
            TAG.button('Add Documents', _class="btn btn-success pull-right", _type="button", _onClick = "window.location='%s'" % URL('add_doc', args=project.id))
        ],
        formstyle='bootstrap3_inline')

    # Assign the project id
    form.vars.project = project.id

    if form.process().accepted:
        response.flash = 'Field Saved'

    # Load existing fields - this is done after form processing so that any new ones are also included
    fields = db(db.field.project==project.id).select()

    return dict(fields=fields, form=form)

@auth.requires_login()
def add_doc():
    """
    Allow users to add docs to a project
    There are two paths
     - loop back to save the doc and add another
     - move forward finish editing

    """
    # Get project or redirect
    try:
        project = db.project(request.args(0,cast=int))
        if project is None:
            raise LookupError
    except:
        redirect(URL('project', 'create'))

    response.title = project.title
    response.subtitle = "Add Document"

    # Construct form for project docs - buttons to save the doc and to move onward in the form
    form = SQLFORM(
        db.doc,
        buttons = [
            TAG.button('Save Document', _class="btn btn-primary", _type="submit"),
            TAG.button('Finish', _class="btn btn-success pull-right", _type="button", _onClick = "window.location='%s'" % URL('view_mine'))
        ],
        formstyle='bootstrap3_inline'
    )

    # Assign the project id
    form.vars.project = project.id

    if form.process().accepted:
        response.flash = 'Document Saved'

    # Load existing docs - this is done after form processing so that any new ones are also included
    docs = db(db.doc.project==project.id).select()

    return dict(docs=docs, form=form)

@auth.requires_login()
def open():
    """
    Allow managers to open their projects for contributions

    """
    # Get project or redirect
    try:
        project = db.project(request.args(0,cast=int))
        if project is None:
            raise LookupError
    except:
        redirect(request.env.http_referer)

    if (project.manager == auth.user_id):
        project.update_record(status=2)

    redirect(URL('project', 'view_mine'))

@auth.requires_login()
def close():
    """
    Allow managers to close their projects

    """
    # Get project or redirect
    try:
        project = db.project(request.args(0,cast=int))
        if project is None:
            raise LookupError
    except:
        redirect(request.env.http_referer)

    if (project.manager == auth.user_id):
        project.update_record(status=1)

    redirect(URL('project', 'view_mine'))

def delete():
    """
    Allow managers to delete their projects

    """
    # Get project or redirect
    try:
        project = db.project(request.args(0,cast=int))
        if project is None:
            raise LookupError
    except:
        redirect(request.env.http_referer)

    if (project.manager == auth.user_id):
        project.delete_record()

    redirect(URL('project', 'view_mine'))
