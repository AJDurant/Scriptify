# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return dict(message=T('Hello World'))


def search():
    if request.vars.q is not None:
        search_request = request.vars.q
    else:
        redirect(URL('static', "404.html"))

    search_term = "%" + search_request + "%"
    
    projects = db((db.project.title).like(search_term)).select()

    if len(projects) is not 0:
        response.title = "Searching for '" + search_request + "'"
        response.subtitle = "Displaying " + str(len(projects)) + " result(s)"
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

    if request.args(0) == 'profile':
        pass

    return locals()
