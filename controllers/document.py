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
    fields = db(db.field.project==doc.project.id).select()

    formfields = []
    for item in fields:
        formfields.append(Field(item.name, type=item.status.fname))

    form = SQLFORM.factory(*formfields,
        submit_button='Contibute',
        formstyle='bootstrap3_inline'
    )

    if form.process().accepted:
        contribid = db.contribution.insert(doc=doc.id, contributor=auth.user_id)
        for (key, value) in dict(form.vars).iteritems():
            items = fields.find(lambda field: field.name == key)

            fieldid = -1
            # web2py is silly this seems to be the only way to actually get a valid Row object from find()
            for item in items:
                fieldid = item.id

            if fieldid != -1:
                db.metadata.insert(contribution=contribid, field=fieldid, data_value=value, status=1)

        session.flash = 'Contribution Saved'
        redirect(URL('project', 'view', args=doc.project.id))
    elif form.errors:
        response.flash = 'Contribution has errors'

    response.title = 'Contribute'
    response.subtitle = doc.name + ' (' + doc.project.title + ')'
    return locals()

@auth.requires_login()
def review():
    """
    Displays document and all contributed fields for accept/reject

    """
    # Get document or redirect
    doc = db.doc(request.args(0,cast=int)) or redirect(request.env.http_referer)

    return dict()
