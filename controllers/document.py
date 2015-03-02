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
    project = db(db.project.id==pid).select().first()
    fields = db(db.field.project==pid).select()
    doc = db(db.doc.project==pid).select()
    form = SQLFORM (db.metadata)
    return dict(form=form, project=project, doc=doc, fields=fields)

def review():
    """
    Displays document and all contributed fields for accept/reject

    """
    return dict()
