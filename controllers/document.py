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
    pid = int (request.vars['pid'])
    docid = int (request.vars['docid'])
    project = db(db.project.id==pid).select().first()
    fields = db(db.field.project==pid).select()
    doc = db(db.doc.id==docid).select().first()
    contribid=db.contribution.insert (doc=doc.id,contributor=auth.user.id)
    """
	Number of problems with this:
	Dynamic number of forms with dynamic fields referencing dynamically documents. (images)
	As of now, this functionality isn't programmed.
	"""
    form = SQLFORM.factory (db.metadata,
    Field ("reference",default=doc.id,readable=False,writable=False),
    Field ("contribution",default=contribid,readable=False,writable=False))
    if form.accepts (request,session):
        redirect (URL('document','contribute.html',vars=dict(pid=pid,docid=docid+1)))
    return dict(form=form, project=project, doc=doc, fields=fields)

def review():
    """
    Displays document and all contributed fields for accept/reject

    """
    return dict()
