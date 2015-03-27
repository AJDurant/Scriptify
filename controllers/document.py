"""
This is the document controller
 - Contribute
 - Review


"""

@auth.requires_login()
def contribute():
    """
    Allows users to contribute to a document
    Displays document image and project fields

    """
    # Get document or redirect
    doc = db.doc(request.args(0,cast=int)) or redirect(request.env.http_referer)
    project = db.project(doc.project)
    fields = db(db.field.project==project.id).select()

    formfields = []
    for item in fields:
        formfields.append(Field(item.name, type=item.status.fname))

    form = SQLFORM.factory(*formfields,
        submit_button='Contibute',
        formstyle='bootstrap3_inline'
    )

    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'

    response.title = 'Contribute'
    response.subtitle = doc.name + ' (' + project.title + ')'
    return locals()

@auth.requires_login()
def review():
    """
    Displays document and all contributed fields for accept/reject

    """
    # Get document or redirect
    doc = db.doc(request.args(0,cast=int)) or redirect(request.env.http_referer)

    return dict()
