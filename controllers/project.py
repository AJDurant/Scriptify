"""
This is the project controller
 - Create
 - Open / Close projects in profile page
 - View


"""

@auth.requires_login()
def create():
    """
    Allows users to create projects
    Include form
    - Project Details
    - Documents
    - Fields

    """
    return dict()

def view():
    """
    Allows users to view a project
    Shows all documents in project
    Links users to contribute to a document

    """
    return dict()
