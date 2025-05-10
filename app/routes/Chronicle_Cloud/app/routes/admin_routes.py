from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, Blog

admin_bp = Blueprint('admin', __name__)

# Route to view all blogs in admin dashboard
@admin_bp.route('/admin/blogs')
def admin_blogs():
    all_blogs = Blog.query.all()
    return render_template('admin_dashboard.html', blogs=all_blogs)

# Route to delete a blog
@admin_bp.route('/admin/delete_blog/<int:blog_id>', methods=['POST'])
def delete_blog(blog_id):
    blog_to_delete = Blog.query.get(blog_id)
    if blog_to_delete:
        db.session.delete(blog_to_delete)
        db.session.commit()
    return redirect(url_for('admin_routes.admin_blogs'))

# Route to edit a blog
@admin_bp.route('/admin/edit_blog/<int:blog_id>', methods=['GET', 'POST'])
def edit_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if request.method == 'POST':
        blog.title = request.form['title']
        blog.content = request.form['content']
        db.session.commit()
        return redirect(url_for('admin_routes.admin_blogs'))
    return render_template('edit_blog.html', blog=blog)
