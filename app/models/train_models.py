import os
import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder

# Ensure 'models' directory exists
os.makedirs('models', exist_ok=True)

# 📘 Emotion Detection Data (30 samples)
emotion_texts = [
    "I am so happy and joyful today!",
    "This is terrible and I feel sad.",
    "I'm angry at how things turned out.",
    "Such a delightful surprise!",
    "Feeling scared and anxious about tomorrow.",
    "Excited about the trip next week!",
    "I’m frustrated with this process.",
    "I feel calm and peaceful.",
    "It’s depressing to think about the past.",
    "I love spending time with my friends.",
    "He ruined my day completely!",
    "I’m worried about my results.",
    "I feel proud of what I achieved.",
    "I am furious about the mistake!",
    "I’m feeling very low today.",
    "It’s such a peaceful morning.",
    "That’s incredibly frustrating.",
    "I'm terrified of failing.",
    "She makes me so happy.",
    "I’m so confused right now.",
    "I’m feeling overwhelmed and tired.",
    "That made my heart so full!",
    "I feel hopeless sometimes.",
    "I can’t stop smiling!",
    "I’m shaking with anger.",
    "My heart is racing with anxiety.",
    "I feel truly relaxed here.",
    "I miss him and feel very alone.",
    "She inspires so much joy in me.",
    "I’m literally trembling with rage."
]
emotion_labels = [
    "happy", "sad", "angry", "happy", "fear",
    "happy", "angry", "calm", "sad", "happy",
    "angry", "fear", "happy", "angry", "sad",
    "calm", "angry", "fear", "happy", "confused",
    "confused", "happy", "sad", "happy", "angry",
    "fear", "calm", "sad", "happy", "angry"
]

# ⚠️ Toxicity Detection Data (30 samples)
toxicity_texts = [
    "You're an idiot.",
    "I hope you have a great day!",
    "This is the dumbest thing ever.",
    "Thank you for your help.",
    "You suck.",
    "What a lovely message!",
    "Shut your mouth!",
    "I really appreciate your effort.",
    "You are the worst!",
    "That's so kind of you.",
    "I hate your stupid face.",
    "Such thoughtful words, thanks!",
    "You're such a loser.",
    "You're awesome!",
    "Nobody cares about you.",
    "That was a very generous thing to do.",
    "Get lost, moron.",
    "You brighten up the room.",
    "Stop being such a jerk.",
    "You handled that well!",
    "I despise everything about you.",
    "Nice job, keep it up!",
    "You make me sick.",
    "It’s been a pleasure working with you.",
    "You're garbage.",
    "You're a kind and wonderful person.",
    "I want to punch you.",
    "Thanks for being there for me.",
    "Why don’t you disappear forever?",
    "You're such a thoughtful friend."
]
toxicity_labels = [
    "toxic", "non-toxic", "toxic", "non-toxic", "toxic",
    "non-toxic", "toxic", "non-toxic", "toxic", "non-toxic",
    "toxic", "non-toxic", "toxic", "non-toxic", "toxic",
    "non-toxic", "toxic", "non-toxic", "toxic", "non-toxic",
    "toxic", "non-toxic", "toxic", "non-toxic", "toxic",
    "non-toxic", "toxic", "non-toxic", "toxic", "non-toxic"
]

# 🧠 Train Emotion Model
emo_vectorizer = TfidfVectorizer()
emo_X = emo_vectorizer.fit_transform(emotion_texts)
emo_label_encoder = LabelEncoder()
emo_y = emo_label_encoder.fit_transform(emotion_labels)
emo_model = LogisticRegression(max_iter=1000)
emo_model.fit(emo_X, emo_y)
joblib.dump((emo_model, emo_vectorizer, emo_label_encoder), 'models/emotion_model.pkl')

# 🧠 Train Toxicity Model
tox_vectorizer = CountVectorizer()
tox_X = tox_vectorizer.fit_transform(toxicity_texts)
tox_y = toxicity_labels
tox_model = MultinomialNB()
tox_model.fit(tox_X, tox_y)
joblib.dump((tox_model, tox_vectorizer), 'models/toxicity_model.pkl')

print("✅ Extended models trained and saved successfully.")
