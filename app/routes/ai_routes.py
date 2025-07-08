from flask import Blueprint, request, render_template
from app.ai.keyword_extractor import extract_keywords
from app.ai.sentiment_analyzer import analyze_sentiment

ai_routes = Blueprint('ai', __name__)

@ai_routes.route('/ai/keywords', methods=['GET', 'POST'])
def keyword_page():
    keywords = []
    input_text = ""

    if request.method == 'POST':
        input_text = request.form.get('content', '')
        if input_text:
            keywords = extract_keywords(input_text)

    return render_template('keyword.html', input_text=input_text, keywords=keywords)

@ai_routes.route('/sentiment', methods=['GET', 'POST'])
def sentiment():
    result = None
    if request.method == 'POST':
        text = request.form.get('text')
        result = analyze_sentiment(text)
    return render_template('sentiment.html', result=result)
