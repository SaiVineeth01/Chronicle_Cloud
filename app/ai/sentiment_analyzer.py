from textblob import TextBlob

# Define keywords to boost sentiment
NEGATIVE_KEYWORDS = ['crashes', 'unreliable', 'lacks', 'fails', 'buggy', 'slow', 'insecure']
POSITIVE_KEYWORDS = ['excellent', 'reliable', 'secure', 'fast', 'intuitive', 'powerful']

def adjust_polarity(text, polarity):
    lowered = text.lower()
    for word in NEGATIVE_KEYWORDS:
        if word in lowered:
            polarity -= 0.3  # apply stronger negativity
    for word in POSITIVE_KEYWORDS:
        if word in lowered:
            polarity += 0.3  # apply stronger positivity
    return max(min(polarity, 1.0), -1.0)  # clip between [-1, 1]

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    # Adjust polarity based on keywords
    polarity = adjust_polarity(text, polarity)

    # Decision logic
    if subjectivity < 0.3 and -0.2 <= polarity <= 0.2:
        sentiment = "Neutral (Technical/Objective)"
    elif polarity > 0.2:
        sentiment = "Positive"
    elif polarity < -0.2:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3)
    }
