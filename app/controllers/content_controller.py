from app import db
from app.models.content import Content

# Function to create content
def create_content(title, body):
    # Create a new Content object and add it to the session
    new_content = Content(title=title, body=body)
    db.session.add(new_content)
    db.session.commit()

# Function to get all content
def get_all_content():
    # Importing here to avoid circular imports
    from app.models.content import Content
    content_list = Content.query.all()  # Fetch all content from the Content table
    return content_list
