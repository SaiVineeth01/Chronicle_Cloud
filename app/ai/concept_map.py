# app/ai/concept_map.py

import spacy
import networkx as nx
from bs4 import BeautifulSoup

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def generate_concept_map(text):
    # Clean HTML if any
    clean_text = BeautifulSoup(text, "html.parser").get_text()

    # Process text with spaCy
    doc = nlp(clean_text)
    G = nx.DiGraph()  # Directed graph

    for sent in doc.sents:
        nouns = [token.text for token in sent if token.pos_ in ["NOUN", "PROPN"]]
        verbs = [token.lemma_ for token in sent if token.pos_ == "VERB"]

        # Add nodes and edges (noun → noun, noun → verb)
        for i in range(len(nouns) - 1):
            G.add_edge(nouns[i], nouns[i + 1])
        for noun in nouns:
            for verb in verbs:
                G.add_edge(noun, verb)

    return nx.node_link_data(G)  # JSON serializable
