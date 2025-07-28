from textblob import TextBlob

# 🔴 Extended Negative Sentiment Keywords
from textblob import TextBlob

# 🔴 Extended Negative Sentiment Keywords (REAL-WORLD TECH/APP/USER FEEDBACK)
NEGATIVE_KEYWORDS = [
    'crashes', 'unreliable', 'lacks', 'fails', 'buggy', 'slow', 'insecure',
    'error', 'issue', 'problem', 'hate', 'poor', 'confusing', 'terrible', 'bad',
    'glitchy', 'freeze', 'laggy', 'annoying', 'useless', 'overpriced', 'complicated',
    'unresponsive', 'frustrating', 'bloated', 'disappointing', 'unintuitive',
    'clunky', 'hard', 'difficult', 'broken', 'waste', 'irrelevant', 'delay',
    'unstable', 'messy', 'inconsistent', 'crash', 'lag', 'slowdown', 'stuck',
    'problematic', 'limitations', 'disaster', 'awkward', 'ugly', 'verbose', 'redundant',
    'conflict', 'interrupts', 'intrusive', 'downtime', 'unhelpful', 'locked',
    'restrictive', 'manual', 'noisy', 'unpleasant', 'nonsense', 'tedious', 'compromise',
    'outdated', 'complex', 'deprecated', 'lousy', 'overwhelming', 'unwanted',
    'misleading', 'annoyed', 'cramped', 'flawed', 'bug', 'errors', 'doesn’t work'
]

# 🟢 Extended Positive Sentiment Keywords (REAL-WORLD TECH/APP/USER FEEDBACK)
POSITIVE_KEYWORDS = [
    'excellent', 'reliable', 'secure', 'fast', 'intuitive', 'powerful',
    'great', 'love', 'amazing', 'smooth', 'efficient', 'awesome', 'helpful',
    'responsive', 'user-friendly', 'affordable', 'clean', 'impressive',
    'flexible', 'useful', 'stable', 'beautiful', 'convenient', 'well-designed',
    'clear', 'simple', 'streamlined', 'robust', 'fantastic', 'outstanding',
    'easy', 'productive', 'effective', 'modern', 'innovative', 'engaging',
    'supportive', 'satisfying', 'flawless', 'optimized', 'neat', 'upgraded',
    'enhanced', 'securely', 'recommend', 'trustworthy', 'smart', 'time-saving',
    'accessible', 'minimal', 'lightweight', 'perfect', 'professional',
    'versatile', 'responsive', 'integrated', 'smoothly', 'quick', 'pleasing',
    'adaptable', 'customizable', 'modular', 'reliable', 'attractive', 'interactive',
    'stable', 'secure', 'organized', 'valuable', 'streamlined', 'clean UI', 'best',
    'loved', 'pleasant', 'error-free', 'neatly built', 'brilliant', 'insightful'
]


def adjust_polarity(text, polarity):
    lowered = text.lower()
    for word in NEGATIVE_KEYWORDS:
        if word in lowered:
            polarity -= 0.2
    for word in POSITIVE_KEYWORDS:
        if word in lowered:
            polarity += 0.2
    return max(min(polarity, 1.0), -1.0)

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    # Adjust polarity using keyword matching
    polarity = adjust_polarity(text, polarity)

    # Decision thresholds
    if subjectivity < 0.3 and -0.25 <= polarity <= 0.25:
        sentiment = "Neutral (Technical/Objective)"
    elif polarity > 0.25:
        sentiment = "Positive"
    elif polarity < -0.25:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3)
    }
