from flask import Blueprint, request, render_template
from app.models import Blog

search_bp = Blueprint('search', __name__)

# Search route to filter blogs by title or content
@search_bp.route('/search', methods=['GET'])
def search_blogs():
    query = request.args.get('query', '')
    blogs = Blog.query.filter(
        (Blog.title.ilike(f'%{query}%')) | (Blog.content.ilike(f'%{query}%'))
    ).all()
    return render_template('search_results.html', blogs=blogs, query=query)
