# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(
                    B('Scriptify'),
                    _class="navbar-brand",
                    _href="/" + request.application
                )
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'IAPT Group 12'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Create a project'), False, URL('project', 'create'), []),
    (T('Browse Projects'), False, URL('project', 'view_open'), []),
    (T('My Projects'), False, URL('project', 'view_mine'), [])
]

if "auth" in locals(): auth.wikimenu()
