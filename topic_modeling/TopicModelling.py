import os
import json
from gensim import corpora, models
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords

# Configuration
DOCUMENT_DIR = '../documents/'  # Folder with your .txt files
OUTPUT_JSON = 'documents/lda_results.json'
NUM_TOPICS = 5  # Number of topics to find

# Load and preprocess documents
def load_documents(directory):
    documents = []
    for filename in sorted(os.listdir(directory)):
        print(filename)
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                documents.append(file.read())
    return documents

def preprocess(text):
    stop_words = set(stopwords.words('english'))
    tokens = simple_preprocess(text, deacc=True)  # Lowercase and remove punctuation
    print(str(tokens))
    return [token for token in tokens if token not in stop_words]

def lda_topic_modeling():
    # Step 1: Load and preprocess documents
    raw_documents = load_documents(DOCUMENT_DIR)
    processed_docs = [preprocess(doc) for doc in raw_documents]

    # Step 2: Create dictionary and corpus
    dictionary = corpora.Dictionary(processed_docs)
    corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
    print(str(corpus))

    # Step 3: Train LDA model
    lda_model = models.LdaModel(corpus=corpus,
                                id2word=dictionary,
                                num_topics=NUM_TOPICS,
                                random_state=42,
                                passes=10)

    # Step 4: Extract topics per document
    results = []
    for i, bow in enumerate(corpus):
        topic_probs = lda_model.get_document_topics(bow)
        dominant_topic = max(topic_probs, key=lambda x: x[1])[0]
        results.append({
            'document_number': i,
            'dominant_topic': int(dominant_topic),
            'topic_distribution': {str(topic): float(prob) for topic, prob in topic_probs}
        })

    # Step 5: Save results to JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

    print(f"✅ LDA results saved to: {OUTPUT_JSON}")

# Run the topic modeling pipeline
if __name__ == '__main__':
    lda_topic_modeling()
