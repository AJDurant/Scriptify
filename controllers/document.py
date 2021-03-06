"""
This is the document controller
 - contribute
 - review

"""

from gluon.custom_import import track_changes; track_changes(True) #enable tracking changes of modules
from bootstrap_widget import BootstrapRadio

def view():
    # Get document or redirect
    try:
        doc = db.doc(request.args(0,cast=int))
        if doc is None:
            raise LookupError
    except:
        redirect(request.env.http_referer)

    # Get fields for the document's project
    fields = db(db.field.project==doc.project.id).select()
    # Get ids of contributions for the doc
    contributions = db(db.contribution.doc == doc.id).select()

    for item in fields:
        # Get accepted metadata for each field
        item.metadata = db((db.metadata.contribution.belongs(contributions)) & (db.metadata.field == item.id) & (db.metadata.status == 2)).select().first()

    response.title = doc.name + ' (' + doc.project.title + ')'
    response.subtitle = 'View'

    session.breadcrumb = []
    session.breadcrumb.append(LI(A(pretty('project'), _href=URL(r=request, c='project', f='index'))))
    session.breadcrumb.append(LI(A(doc.project.title, _href=URL(r=request, c='project', f='view', args=doc.project))))
    session.breadcrumb.append(LI(A(doc.name, _href=URL(r=request, c=request.controller, f=request.function, args=request.args))))

    return locals()

@auth.requires_login()
def contribute():
    """
    Allows users to contribute to a document
    Displays document image and project fields

    """
    # Get document or redirect
    try:
        doc = db.doc(request.args(0,cast=int))
        if doc is None:
            raise LookupError
    except:
        redirect(request.env.http_referer)

    # Get fields for the document's project
    fields = db(db.field.project==doc.project.id).select()
    # Get ids of contributions for the doc
    contributions = db(db.contribution.doc == doc.id).select()

    # Construct a list of fields for use in a form factory, with the defined field type
    formfields = []
    for item in fields:
        # Check if field has accepted data
        accept = db((db.metadata.contribution.belongs(contributions)) & (db.metadata.field == item.id) & (db.metadata.status == 2)).select()
        if accept:
            continue
        formfields.append(Field(item.name, type=item.status.fname))

    # Construct an SQLFORM from the generated list of fields
    form = SQLFORM.factory(*formfields,
        submit_button='Contibute',
        formstyle='bootstrap3_inline'
    )

    if form.process().accepted:
        # Create a new contribution to link metadata to
        contribid = db.contribution.insert(doc=doc.id, contributor=auth.user_id)

        # Insert each submitted field into the db for the contribution
        for (key, value) in dict(form.vars).iteritems():
            items = fields.find(lambda field: field.name == key)

            fieldid = -1
            # web2py is silly this seems to be the only way to actually get a valid Row object from find()
            for item in items:
                fieldid = item.id

            if fieldid != -1: # Only use valid fields
                db.metadata.insert(contribution=contribid, field=fieldid, data_value=value, status=1)

        session.flash = 'Contribution Saved'
        redirect(URL('project', 'view', args=doc.project.id))
    elif form.errors:
        response.flash = 'Contribution has errors'

    response.title = doc.name + ' (' + doc.project.title + ')'
    response.subtitle = 'Contribute'

    session.breadcrumb = []
    session.breadcrumb.append(LI(A(pretty('project'), _href=URL(r=request, c='project', f='index'))))
    session.breadcrumb.append(LI(A(doc.project.title, _href=URL(r=request, c='project', f='view', args=doc.project))))
    session.breadcrumb.append(LI(A(doc.name, _href=URL(r=request, c='document', f='view', args=doc.id))))
    session.breadcrumb.append(LI(A(T(pretty(request.function)), _href=URL(r=request, c=request.controller, f=request.function, args=request.args))))

    response.view = 'document/doc.html'
    return locals()

@auth.requires_login()
def review():
    """
    Displays document and all contributed fields for accept/reject

    """
    # Get document or redirect
    try:
        doc = db.doc(request.args(0,cast=int))
        if doc is None:
            raise LookupError
    except:
        redirect(URL('project', 'view_mine'))

    # Only allow managers to review documents
    if (doc.project.manager != auth.user_id):
        redirect(URL('project', 'view_mine'))

    # Get fields for the document's project
    fields = db(db.field.project==doc.project.id).select()
    # Get ids of contributions for the doc
    contributions = db(db.contribution.doc == doc.id).select()

    # Construct a list of field metadata for use in a form factory
    formfields = []
    for item in fields:
        # Check if field has accepted data
        accept = db((db.metadata.contribution.belongs(contributions)) & (db.metadata.field == item.id) & (db.metadata.status == 2)).select()
        if accept:
            continue

        # Get metadata for each field
        item.metadata = db((db.metadata.contribution.belongs(contributions)) & (db.metadata.field == item.id) & (db.metadata.status == 1)).select()
        # Construct fields
        if item.metadata:
            field_options = [(contrib.id, contrib.data_value) for contrib in item.metadata]
            field_options.append((0, 'Reject Contributions'))
            formfields.append(
                Field(
                    item.name,
                    type='list:string',
                    requires=IS_IN_SET(field_options),
                    widget=BootstrapRadio.widget
                )
            )

    # If there are metadata - Construct the form
    if formfields:
        # Construct an SQLFORM from the generated list of fields
        form = SQLFORM.factory(*formfields,
            submit_button='Submit Review',
            formstyle='bootstrap3_inline'
        )

        if form.process().accepted:

            for (key, value) in dict(form.vars).iteritems():
                # Get the fieldid for each submitted field
                fieldid = -1
                items = fields.find(lambda field: field.name == key)
                # web2py is silly this seems to be the only way to actually get a valid Row object from find()
                for item in items:
                    fieldid = item.id

                if fieldid != -1: # Only use valid fields
                    # Reject all metadata for the field
                    db((db.metadata.contribution.belongs(contributions)) & (db.metadata.field == fieldid)).update(status=3)

                    # Accept selected metadata
                    if value != 0:
                        db(db.metadata.id == value).update(status=2)

            session.flash = 'Review Saved'
            redirect(URL('project', 'view', args=doc.project.id))
        elif form.errors:
            response.flash = 'Review has errors'
    else:
        form = "No pending contributions"

    response.title = doc.name + ' (' + doc.project.title + ')'
    response.subtitle = 'Review'

    session.breadcrumb = []
    session.breadcrumb.append(LI(A(pretty('project'), _href=URL(r=request, c='project', f='index'))))
    session.breadcrumb.append(LI(A(doc.project.title, _href=URL(r=request, c='project', f='view', args=doc.project))))
    session.breadcrumb.append(LI(A(doc.name, _href=URL(r=request, c='document', f='view', args=doc.id))))
    session.breadcrumb.append(LI(A(T(pretty(request.function)), _href=URL(r=request, c=request.controller, f=request.function, args=request.args))))

    response.view = 'document/doc.html'
    return locals()
