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
    (T('Browse Projects'), False, URL('project', 'index'), []),
    (T('My Projects'), False, URL('project', 'view_mine'), [])
]

if "auth" in locals(): auth.wikimenu()

session.breadcrumb = None

# make links pretty by capitalizing and using 'home' instead of 'default'
def pretty (s):
    return s.replace('default', 'home').replace('_', ' ').capitalize()

def breadcrumbs(custom=None):
    """
    Create breadcrumb links for current request
    """

    menus = [LI(A(T('Home'), _href=URL(r=request, c='default', f='index')))]

    if custom:
        menus.extend(custom)
    elif request.controller != 'default':
       # add link to current controller
       menus.append(LI(A(T(pretty(request.controller)), _href=URL(r=request, c=request.controller, f='index'))))
       if request.function == 'index':
           # are at root of controller
           pass
       else:
           # are at function within controller
           menus.append(LI(A(T(pretty(request.function)), _href=URL(r=request, c=request.controller, f=request.function))))
    else:
       if request.function == 'index':
           # are at root of controller
           pass
       else:
           # are at function within controller
           menus.append(LI(A(T(pretty(request.function)), _href=URL(r=request, c=request.controller, f=request.function))))

    return XML(' '.join(str(m) for m in menus))
