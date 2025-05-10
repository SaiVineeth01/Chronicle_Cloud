from flask import Blueprint, request, jsonify
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from rake_nltk import Rake
import gensim
from gensim import corpora

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences_count=3)
    result = ' '.join(str(sentence) for sentence in summary)
    return jsonify({'summary': result})


@ai_bp.route('/extract_keywords', methods=['POST'])
def extract_keywords():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    rake = Rake()
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases()
    return jsonify({'keywords': keywords})


@ai_bp.route('/topic_model', methods=['POST'])
def topic_model():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Split text into sentences or simple list for topic modeling
    texts = [text.lower().split()]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=1, id2word=dictionary, passes=15)
    topics = lda_model.print_topics(num_words=5)
    return jsonify({'topics': topics})
