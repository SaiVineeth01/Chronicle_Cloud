from flask import Blueprint, render_template, redirect, url_for, request
from app.controllers.content_controller import create_content, get_all_content

content_bp = Blueprint('content', __name__)

# Route to display all content
@content_bp.route('/content')
def content():
    contents = get_all_content()
    return render_template('content.html', contents=contents)

# Route to create new content (POST request)
@content_bp.route('/create_content', methods=['POST'])
def create():
    title = request.form['title']
    body = request.form['body']
    create_content(title, body)
    return redirect(url_for('content.content'))
