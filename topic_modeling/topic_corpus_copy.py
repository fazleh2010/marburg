import json
from gensim import corpora, models
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
import nltk

# Download stopwords if not already downloaded
nltk.download('stopwords')

# Example corpus: List of text documents
corpus = [
    "The economy is working better than ever. NASA discovered water on Mars. Stock markets show unprecedented growth. "
    "SpaceX plans to launch a new rocket into orbit. Interest rates are expected to rise next year. Astronauts are preparing for a mission to the moon."
]

NUM_TOPICS = 3  # Adjust as needed
OUTPUT_JSON = '/home/melahi/code/marburg/documents/lda_results_from_corpus.json'

# Preprocessing function
def preprocess(text):
    stop_words = set(stopwords.words('english'))
    tokens = simple_preprocess(text, deacc=True)
    return [token for token in tokens if token not in stop_words]

def lda_topic_modeling_from_corpus(text_corpus):
    # Step 1: Preprocess
    processed_docs = [preprocess(doc) for doc in text_corpus]

    # Step 2: Create dictionary and bag-of-words corpus
    dictionary = corpora.Dictionary(processed_docs)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    # Step 3: Train LDA model
    lda_model = models.LdaModel(
        corpus=bow_corpus,
        id2word=dictionary,
        num_topics=NUM_TOPICS,
        random_state=42,
        passes=10
    )

    # Step 4: Extract dominant topic per document
    doc_results = []
    for i, (original_text, bow) in enumerate(zip(text_corpus, bow_corpus)):
        topic_probs = lda_model.get_document_topics(bow)
        dominant_topic = max(topic_probs, key=lambda x: x[1])[0]
        doc_results.append({
            'document_number': i,
            'text': original_text,
            'dominant_topic': int(dominant_topic),
            'topic_distribution': {
                str(topic): float(prob) for topic, prob in topic_probs
            }
        })

    # Step 5: Extract topic keywords
    topic_results = []
    for topic_id in range(NUM_TOPICS):
        words = lda_model.show_topic(topic_id, topn=10)
        topic_results.append({
            'topic_number': topic_id,
            'keywords': [word for word, prob in words]
        })

    # Step 6: Save both results to JSON
    output = {
        'topics': topic_results,
        'documents': doc_results
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"✅ Results saved to: {OUTPUT_JSON}")

# Run the LDA pipeline
lda_topic_modeling_from_corpus(corpus)
