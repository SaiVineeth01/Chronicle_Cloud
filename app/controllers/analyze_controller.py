import os
import re
import joblib
import spacy
from textblob import TextBlob
from langdetect import detect
from flask import request, jsonify
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np  # in case some outputs are numpy types

# Load spaCy English model for entity recognition
nlp = spacy.load("en_core_web_sm")

# Load models from models/ folder
base_dir = os.path.dirname(os.path.abspath(__file__))

emo_model, emo_vectorizer, emo_label_encoder = joblib.load(
    os.path.join(base_dir, '..', 'models', 'emotion_model.pkl')
)

tox_model, tox_vectorizer = joblib.load(
    os.path.join(base_dir, '..', 'models', 'toxicity_model.pkl')
)

# --- Utility Functions ---
def clean_text(text):
    return re.sub(r"[^a-zA-Z\s]", "", text.lower().strip())

def to_serializable(val):
    if hasattr(val, 'tolist'):
        return val.tolist()
    elif isinstance(val, (np.integer, np.floating)):
        return val.item()
    return val

# --- Language Detection ---
def detect_language(text):
    return detect(text)

# --- Entity Extraction ---
def extract_entities(text):
    doc = nlp(text)
    return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

# --- Spelling Correction ---
def correct_spelling(text):
    blob = TextBlob(text)
    return str(blob.correct())

# --- Emotion Detection ---
def detect_emotion(text):
    cleaned = clean_text(text)
    X = emo_vectorizer.transform([cleaned])
    label_idx = int(emo_model.predict(X)[0])  # Cast to Python int
    emotion = emo_label_encoder.inverse_transform([label_idx])[0]
    return str(emotion)

# --- Toxicity Detection ---
def detect_toxicity(text):
    cleaned = clean_text(text)
    X = tox_vectorizer.transform([cleaned])
    prediction = tox_model.predict(X)[0]
    return str(prediction)  # e.g., "toxic", "non-toxic"

# --- Topic Modeling ---
def extract_topics(text, n_topics=1, n_words=5):
    cleaned = clean_text(text)
    vectorizer = CountVectorizer(stop_words='english', ngram_range=(1, 2))
    X = vectorizer.fit_transform([cleaned])
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)
    terms = vectorizer.get_feature_names_out()
    topics = []
    for idx, topic in enumerate(lda.components_):
        top_terms = [terms[i] for i in topic.argsort()[-n_words:][::-1]]
        topics.append({"Topic": f"Topic {idx + 1}", "Keywords": top_terms})
    return topics

# --- Flask Route Logic (optional if used directly) ---
def analyze_text_controller():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "Text input is required."}), 400

    result = {
        "emotion": detect_emotion(text),
        "toxicity": detect_toxicity(text),
        "language": detect_language(text),
        "entities": extract_entities(text),
        "topics": extract_topics(text),
        "corrected": correct_spelling(text)
    }

    # Ensure everything is serializable
    result = {k: to_serializable(v) for k, v in result.items()}
    return jsonify(result)
