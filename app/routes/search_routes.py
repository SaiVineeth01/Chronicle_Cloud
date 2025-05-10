from flask import Blueprint, request, render_template
from app.controllers.content_controller import get_all_content

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    contents = get_all_content()
    filtered = [content for content in contents if query.lower() in content.title.lower()]
    return render_template('search.html', contents=filtered)
