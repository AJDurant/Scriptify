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
    return dict()

def review():
    """
    Displays document and all contributed fields for accept/reject

    """
    return dict()
