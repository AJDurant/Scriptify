"""
This is the main application controller
 - index
 - search
 - user
 - download

"""

def index():
    """
    Home page of Scriptify
    This displays the 5 latest porjects (that are open)

    """
    response.title = "Welcome to Scriptify"
    response.subtitle = "Latest Projects"
    # Get 5 latest open projects
    projects = db((db.project.id > 0) & (db.project.status == 2)).select(orderby=~db.project.id, limitby=(0, 6))

    return dict(projects = projects)


def search():
    """
    Search Results page
    displays all projects that match the search term given by q in the request

    """
    if request.vars.q is not None:
        search_request = request.vars.q
    else:
        redirect(URL('static', "404.html"))

    search_term = "%" + search_request + "%"

    # Get open projects that match the search term
    projects = db((db.project.title).like(search_term) & (db.project.status == 2)).select()

    if len(projects) is not 0:
        response.title = "Searching for '" + search_request + "'"
        response.subtitle = "Displaying " + str(len(projects)) + (" result" if len(projects) == 1 else " results")
    else:
        response.title = "No results for '" + search_request + "'"

    return dict(projects = projects)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """

    form = auth()

    response.title = "Scriptify"

    return locals()

def download():
    """
    Allows access to uploaded media (images)

    """
    return response.download(request, db)
