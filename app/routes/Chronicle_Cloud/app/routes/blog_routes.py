from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, Blog, Comment  # Import Comment model if needed

blog_bp = Blueprint('blog', __name__)

# Route to view all blogs
@blog_bp.route('/blogs')
def blogs():
    all_blogs = Blog.query.all()  # Fetch all blogs from DB
    return render_template('blogs.html', blogs=all_blogs)  # Send to template

# Route to create a new blog
@blog_bp.route('/create_blog', methods=['GET', 'POST'])
def create_blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_blog = Blog(title=title, content=content, user_id=1)  # user_id might need to be dynamically set
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('blog.blogs'))  # Corrected: Use 'blog.blogs' since it's defined in the blog_bp blueprint
    return render_template('create_blog.html')

# Route to view blog details and comments
@blog_bp.route('/blog/<int:blog_id>')
def blog_details(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    comments = Comment.query.filter_by(blog_id=blog_id).all()  # Fetch comments related to the blog
    return render_template('blog_details.html', blog=blog, comments=comments)

# Route to post a comment
@blog_bp.route('/comment/<int:blog_id>', methods=['POST'])
def post_comment(blog_id):
    content = request.form['content']
    new_comment = Comment(blog_id=blog_id, content=content)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('blog.blog_details', blog_id=blog_id))  # Redirect to blog details page

