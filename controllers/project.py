"""
This is the project controller
 - Create
 - Open / Close projects in profile page
 - View


"""

def view_open():
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
    project_id = request.args[0] # Get from URL
    project = db(db.project.id == project_id).select().first()
    documents = db(db.doc.project == project_id).select()
    response.title = project.title
    return dict(project=project, documents=documents)

@auth.requires_login()
def view_mine():
    """
    Allow users to view all projects that they created

    """
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
    form = SQLFORM(db.project)
    form.vars.manager = auth.user_id
    form.vars.status = 1 # Project status - closed.
    if form.process().accepted:
        response.flash = 'record inserted'
        redirect(URL('project', 'view_mine'))
    return dict(form=form, cat="This is my cat")

@auth.requires_login()
def open():
    """
    Allow managers to open their projects for contributions

    """
    project_id = request.args[0] # Get from URL
    project = db(db.project.id == project_id).select().first()
    if (project.manager == auth.user_id):
        project.update_record(status=2)

    redirect(URL('project', 'view_mine'))

@auth.requires_login()
def close():
    """
    Allow managers to close their projects

    """
    project_id = request.args[0] # Get from URL
    project = db(db.project.id == project_id).select().first()
    if (project.manager == auth.user_id):
        project.update_record(status=1)
    redirect(URL('project', 'view_mine'))

def delete():
    """
    Allow managers to delete their projects

    """
    project_id = request.args[0] # Get from URL
    project = db(db.project.id == project_id).select().first()
    if (project.manager == auth.user_id):
        project.delete_record()
    redirect(URL('project', 'view_mine'))
