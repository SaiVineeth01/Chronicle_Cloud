import yake

def extract_keywords(text, max_keywords=10):
    kw_extractor = yake.KeywordExtractor(lan="en", n=1, top=max_keywords)
    keywords = kw_extractor.extract_keywords(text)
    return [kw for kw, score in keywords]
