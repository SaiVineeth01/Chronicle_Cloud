from flask import Blueprint, request, jsonify 
from app.controllers.analyze_controller import (
    detect_language, extract_entities, correct_spelling,
    detect_toxicity, detect_emotion, extract_topics
)

analyze_bp = Blueprint('analyze', __name__, url_prefix='/analyze')
toxicity_bp = Blueprint('toxicity', __name__, url_prefix='/toxicity')

@analyze_bp.route('/language', methods=['POST'])
def analyze_language():
    try:
        text = request.json.get('text', '')
        result = detect_language(text)
        return jsonify({'language': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyze_bp.route('/entities', methods=['POST'])
def analyze_entities():
    try:
        text = request.json.get('text', '')
        result = extract_entities(text)
        return jsonify({'entities': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyze_bp.route('/spellcheck', methods=['POST'])
def analyze_spellcheck():
    try:
        text = request.json.get('text', '')
        result = correct_spelling(text)
        return jsonify({'corrected_text': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyze_bp.route('/emotion', methods=['POST'])
def analyze_emotion():
    try:
        text = request.json.get('text', '')
        result = detect_emotion(text)
        return jsonify({'emotion': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyze_bp.route('/topics', methods=['POST'])
def analyze_topics():
    try:
        text = request.json.get('text', '')
        result = extract_topics(text)
        return jsonify({'topics': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@toxicity_bp.route('/check', methods=['POST'])
def check_toxicity():
    try:
        text = request.json.get('text', '')
        result = detect_toxicity(text)
        return jsonify({'toxicity': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500