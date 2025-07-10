import os
import re
from langdetect import detect
from spellchecker import SpellChecker
import spacy
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Load NLP model
nlp = spacy.load("en_core_web_sm")
spell = SpellChecker()

# Base directory
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Paths to models and vectorizers
toxicity_model_path = os.path.join(base_dir, 'models', 'toxicity_model.pkl')
tox_vectorizer_path = os.path.join(base_dir, 'models', 'tox_vectorizer.pkl')

emotion_model_path = os.path.join(base_dir, 'models', 'emotion_model.pkl')
emo_vectorizer_path = os.path.join(base_dir, 'models', 'vectorizer.pkl')

# ✅ Load models and their corresponding vectorizers
toxicity_model = joblib.load(toxicity_model_path)
tox_vectorizer = joblib.load(tox_vectorizer_path)

emotion_model = joblib.load(emotion_model_path)
emo_vectorizer = joblib.load(emo_vectorizer_path)

# ✅ Clean text
def clean_text(text):
    return re.sub(r'[^a-zA-Z\s]', '', text.lower().strip())

# ✅ Language detection
def detect_language(text):
    return detect(text)

# ✅ Named Entity Recognition
def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# ✅ Spell correction
def correct_spelling(text):
    words = text.split()
    corrected = [spell.correction(word) or word for word in words]
    return " ".join(corrected)

# ✅ Toxicity detection
def detect_toxicity(text):
    cleaned = clean_text(text)
    X = tox_vectorizer.transform([cleaned])
    return toxicity_model.predict(X)[0]

# ✅ Emotion detection
def detect_emotion(text):
    cleaned = clean_text(text)
    X = emo_vectorizer.transform([cleaned])
    return emotion_model.predict(X)[0]

# ✅ Topic extraction using LDA
def extract_topics(text, n_topics=2, n_words=5):
    cleaned = clean_text(text)
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform([cleaned])
    
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)

    topics = []
    terms = vectorizer.get_feature_names_out()
    for idx, topic in enumerate(lda.components_):
        top_terms = [terms[i] for i in topic.argsort()[-n_words:][::-1]]
        topics.append((f"Topic {idx+1}", top_terms))
    return topics
