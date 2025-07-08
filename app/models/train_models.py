import os
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Sample training data for toxicity detection
toxicity_texts = [
    "You are so stupid", "I hate you", "You are amazing",
    "This is horrible", "You're lovely", "Terrible person",
    "Great job", "You suck", "Nice effort", "Worst ever"
]
toxicity_labels = [1, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # 1 = toxic, 0 = non-toxic

# Sample training data for emotion detection
emotion_texts = [
    "I am so happy today",     # happy
    "This is a sad moment",    # sad
    "I'm so angry at you",     # angry
    "I feel nothing",          # neutral
    "What a joyful day",       # happy
    "Everything is terrible",  # sad
    "I’m furious right now",   # angry
    "Just a normal day",       # neutral
    "Ecstatic and grateful",   # happy
    "This is disappointing"    # sad
]
emotion_labels = [
    "happy", "sad", "angry", "neutral",
    "happy", "sad", "angry", "neutral",
    "happy", "sad"
]

# Create vectorizers
tox_vectorizer = CountVectorizer()
emo_vectorizer = CountVectorizer()

# Transform input
tox_X = tox_vectorizer.fit_transform(toxicity_texts)
emo_X = emo_vectorizer.fit_transform(emotion_texts)

# Train models
tox_model = LogisticRegression()
tox_model.fit(tox_X, toxicity_labels)

emo_model = LogisticRegression()
emo_model.fit(emo_X, emotion_labels)

# ✅ Ensure model folder exists
model_dir = os.path.join("..", "app", "models")
os.makedirs(model_dir, exist_ok=True)

# Save model files
tox_path = os.path.join(model_dir, "toxicity_model.pkl")
emo_path = os.path.join(model_dir, "emotion_model.pkl")

joblib.dump((tox_model, tox_vectorizer), tox_path)
joblib.dump((emo_model, emo_vectorizer), emo_path)

print("[✔] Models with neutral class saved successfully in app/models/")
