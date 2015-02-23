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
    fields = db(db.field.project==pid).select().first()
    doc = db(db.doc.project==pid).select().first()
    form = SQLFORM (db.field, fields)
    return dict(form=form, doc=doc)

def review():
    """
    Displays document and all contributed fields for accept/reject

    """
    return dict()
