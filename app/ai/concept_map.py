import spacy
import networkx as nx
from bs4 import BeautifulSoup
from networkx.readwrite import json_graph

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def generate_concept_map(text):
    # Clean HTML tags
    clean_text = BeautifulSoup(text, "html.parser").get_text()
    doc = nlp(clean_text)

    G = nx.DiGraph()

    for sent in doc.sents:
        span = sent.as_doc()

        # Extract subjects, verbs, and objects more accurately
        subjects = [token for token in span if token.dep_ in ("nsubj", "nsubjpass")]
        verbs = [token for token in span if token.pos_ == "VERB"]
        objects = [token for token in span if token.dep_ in ("dobj", "pobj", "attr", "oprd")]

        for subj in subjects:
            for verb in verbs:
                G.add_edge(subj.lemma_.lower(), verb.lemma_.lower())
                for obj in objects:
                    G.add_edge(verb.lemma_.lower(), obj.lemma_.lower())

    # Optionally add named entities as relationships
    for ent in doc.ents:
        if ent.label_ in ("ORG", "PERSON", "GPE", "EVENT"):
            G.add_node(ent.text.strip())

    return json_graph.node_link_data(G, edges="links")

