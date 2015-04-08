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

session.titleargs = None

def breadcrumbs(arg_title=None):
   """
   Create breadcrumb links for current request
   """
   # make links pretty by capitalizing and using 'home' instead of 'default'
   pretty = lambda s: s.replace('default', 'home').replace('_', ' ').capitalize()
   menus = [LI(A(T('Home'), _href=URL(r=request, c='default', f='index')))]
   if request.controller != 'default':
       # add link to current controller
       menus.append(LI(A(T(pretty(request.controller)), _href=URL(r=request, c=request.controller, f='index'))))
       if request.function == 'index':
           # are at root of controller
           menus[-1] = LI(A(T(pretty(request.controller)), _href=URL(r=request, c=request.controller, f=request.function)))
       else:
           # are at function within controller
           menus.append(LI(A(T(pretty(request.function)), _href=URL(r=request, c=request.controller, f=request.function))))
       # you can set a title putting using breadcrumbs('My Detail Title')
       if request.args and arg_title:
           menus.append(LI(A(T(arg_title)), _href=URL(r=request, c=request.controller, f=request.function,args=[request.args])))
   else:
       if request.function == 'index':
           # are at root of controller
           pass
       else:
           # are at function within controller
           menus.append(LI(A(T(pretty(request.function)), _href=URL(r=request, c=request.controller, f=request.function))))
       # you can set a title putting using breadcrumbs('My Detail Title')
       if request.args and arg_title:
           menus.append(LI(A(T(arg_title), _href=URL(r=request, f=request.function,args=[request.args]))))

   return XML(' '.join(str(m) for m in menus))
