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
label_to_emotion = {
    0: "joy",
    1: "sadness",
    2: "anger",
    3: "fear",
    4: "love",
    5: "surprise",
    6: "disgust",
    7: "trust",
    8: "anticipation",
    9: "neutral"
}


# Helpers
def clean_text(text):
    return re.sub(r'[^a-zA-Z\s]', '', text.lower().strip())

# NLP Tools
def detect_language(text):
    return detect(text)

def extract_entities(text):
    doc = nlp(text)
    return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

def correct_spelling(text):
    words = text.split()
    corrected = [spell.correction(word) or word for word in words]
    return " ".join(corrected)

def detect_toxicity(text):
    cleaned = clean_text(text)
    X = tox_vectorizer.transform([cleaned])
    return "Toxic" if int(toxicity_model.predict(X)[0]) == 1 else "Non-Toxic"

def detect_emotion(text):
    cleaned = clean_text(text)
    X = emo_vectorizer.transform([cleaned])
    label = int(emotion_model.predict(X)[0])
    return label_to_emotion.get(label, "unknown")

def extract_topics(text, n_topics=1, n_words=5):
    cleaned = clean_text(text)
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform([cleaned])
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)
    terms = vectorizer.get_feature_names_out()
    topics = []
    for idx, topic in enumerate(lda.components_):
        top_terms = [terms[i] for i in topic.argsort()[-n_words:][::-1]]
        topics.append({"Topic": f"Topic {idx + 1}", "Keywords": top_terms})
    return topics
