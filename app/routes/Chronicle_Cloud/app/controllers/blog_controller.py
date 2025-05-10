from app.models.blog import Blog

# Fetch blogs from the database with pagination
def get_blogs(page):
    per_page = 5
    blogs = Blog.query.paginate(page, per_page, False)
    previous_page = blogs.prev_num if blogs.has_prev else None
    next_page = blogs.next_num if blogs.has_next else None
    return blogs.items, previous_page, next_page, blogs.page, blogs.pages

# Create a new blog
def create_blog(title, content, tags):
    new_blog = Blog(title=title, content=content, tags=tags)
    db.session.add(new_blog)
    db.session.commit()


