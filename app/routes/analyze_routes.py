from flask import Blueprint, request, jsonify
from app.controllers.analyze_controller import (
    detect_toxicity, detect_language, extract_entities,
    correct_spelling, detect_emotion, extract_topics
)

analyze_bp = Blueprint('analyze', __name__, url_prefix='/analyze')

@analyze_bp.route('/language', methods=['POST'])
def analyze_language():
    text = request.json.get('text', '')
    return jsonify({'language': detect_language(text)})

@analyze_bp.route('/entities', methods=['POST'])
def analyze_entities():
    text = request.json.get('text', '')
    return jsonify({'entities': extract_entities(text)})

@analyze_bp.route('/spellcheck', methods=['POST'])
def spellcheck():
    text = request.json.get('text', '')
    return jsonify({'corrected': correct_spelling(text)})

@analyze_bp.route('/emotion', methods=['POST'])
def analyze_emotion():
    text = request.json.get('text', '')
    return jsonify({'emotion': detect_emotion(text)})

@analyze_bp.route('/topics', methods=['POST'])
def analyze_topics():
    text = request.json.get('text', '')
    return jsonify({'topics': extract_topics(text)})

# Toxicity detection
toxicity_bp = Blueprint('toxicity', __name__, url_prefix='/toxicity')

@toxicity_bp.route('/check', methods=['POST'])
def check_toxicity():
    text = request.json.get('text', '')
    return jsonify({'toxic': detect_toxicity(text)})
