# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()


# Setup db object
db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])


## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()


# Define custom user table
db.define_table(
    auth.settings.table_user_name,
    Field('username', length=128, unique=True, comment='Unique name used for login, and publicly on the website'),
    Field('first_name', length=128, default='', label='First Name', comment='Your first name'),
    Field('last_name', length=128, default='', label='Last Name', comment='Your last name'),
    Field('email', length=128, default='', unique=True),                                    # required
    Field('password', 'password', length=512, readable=False, label='Password'),            # required
    Field('registration_key', length=512, writable=False, readable=False, default=''),      # required
    Field('reset_password_key', length=512, writable=False, readable=False, default=''),    # required
    Field('registration_id', length=512, writable=False, readable=False, default=''),       # required
    format='%(first_name)s %(last_name)s (%(username)s)')

## User validators
custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.username.requires = [IS_NOT_EMPTY(error_message=auth.messages.is_empty), IS_NOT_IN_DB(db, custom_auth_table.username)]
custom_auth_table.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [IS_STRONG(min=6, upper=1, number=1, special=0), CRYPT()]
custom_auth_table.email.requires = [
    IS_EMAIL(error_message=auth.messages.invalid_email),
    IS_NOT_IN_DB(db, custom_auth_table.email)]

# tell auth to use custom_auth_table
auth.settings.table_user = custom_auth_table


## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# set formstyle to nice bootstrap
auth.settings.formstyle = 'bootstrap3_inline'
