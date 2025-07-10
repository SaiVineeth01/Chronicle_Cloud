import os
import re
from langdetect import detect
from spellchecker import SpellChecker
import spacy
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Load spaCy model and spell checker
nlp = spacy.load("en_core_web_sm")
spell = SpellChecker()

# Base dir
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Load models
toxicity_model = joblib.load(os.path.join(base_dir, 'models', 'toxicity_model.pkl'))
tox_vectorizer = joblib.load(os.path.join(base_dir, 'models', 'tox_vectorizer.pkl'))

emotion_model = joblib.load(os.path.join(base_dir, 'models', 'emotion_model.pkl'))
emo_vectorizer = joblib.load(os.path.join(base_dir, 'models', 'vectorizer.pkl'))

# Helpers
def clean_text(text):
    return re.sub(r'[^a-zA-Z\s]', '', text.lower().strip())

# 1. Language Detection
def detect_language(text):
    return detect(text)

# 2. Named Entity Recognition
def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# 3. Spell Correction
def correct_spelling(text):
    words = text.split()
    corrected = [spell.correction(word) or word for word in words]
    return " ".join(corrected)

# 4. Toxicity Detection
def detect_toxicity(text):
    cleaned = clean_text(text)
    X = tox_vectorizer.transform([cleaned])
    return int(toxicity_model.predict(X)[0])

# 5. Emotion Detection
def detect_emotion(text):
    cleaned = clean_text(text)
    X = emo_vectorizer.transform([cleaned])
    return emotion_model.predict(X)[0]

# 6. Topic Modeling
def extract_topics(text, n_topics=1, n_words=5):
    cleaned = clean_text(text)
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform([cleaned])
    
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)

    topics = []
    terms = vectorizer.get_feature_names_out()
    for idx, topic in enumerate(lda.components_):
        top_terms = [terms[i] for i in topic.argsort()[-n_words:][::-1]]
        topics.append({"Topic": f"Topic {idx + 1}", "Keywords": top_terms})
    return topics
