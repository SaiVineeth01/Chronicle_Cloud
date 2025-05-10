from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import Blog
from app import db
from flask_login import login_required, current_user
from app.controllers.blog_controller import save_blog

# Create a Blueprint instance for blogs
blog_bp = Blueprint('blogs', __name__)

# View all blogs
@blog_bp.route('/view_blogs')
def view_blogs():
    blogs = Blog.query.all()  # Fetch all blogs from the database
    return render_template('view_blogs.html', blogs=blogs)

# Route to render blogs.html (NEW ROUTE you requested)
@blog_bp.route('/blogs')
def blogs_page():
    blogs = Blog.query.all()
    return render_template('blogs.html', blogs=blogs)

# Create a new blog (POST request)
@blog_bp.route('/blogs/create', methods=['POST'])
@login_required
def create_new_blog():
    title = request.form['title']
    category = request.form.get('category')
    content = request.form['content']

    # Check if both title and content are provided
    if not title or not content:
        flash("Title and content are required!", "danger")
        return redirect(url_for('blogs.create_blog'))

    # Call the controller function to create the blog
    if save_blog(title, category, content, current_user.id):
        flash("Blog created successfully!", "success")
    else:
        flash("There was an error creating the blog. Please try again.", "danger")

    return redirect(url_for('blogs.view_blogs'))

# Delete a specific blog
@blog_bp.route('/blogs/delete/<int:blog_id>', methods=['POST'])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    # Ensure the current user is the owner of the blog before allowing deletion
    if blog.user_id != current_user.id:
        flash("You are not authorized to delete this blog", "danger")
        return redirect(url_for('blogs.view_blogs'))

    try:
        db.session.delete(blog)
        db.session.commit()
        flash("Blog deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error deleting blog. Please try again.", "danger")

    return redirect(url_for('blogs.view_blogs'))

# Render the create_blog.html page (GET request)
@blog_bp.route('/blogs/create', methods=['GET'])
@login_required
def create_blog():
    return render_template('create_blog.html')
