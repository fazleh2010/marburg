import os
import json
from gensim import corpora, models
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
import nltk

# Download stopwords if not already downloaded
nltk.download('stopwords')

# Parameters
CORPUS_DIR = '/home/melahi/code/marburg/documents/corpus_texts'  # Input folder
OUTPUT_DIR = '/home/melahi/code/marburg/documents/lda_per_file_output'  # Output folder
NUM_TOPICS = 3

# Make sure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Preprocessing function
def preprocess(text):
    stop_words = set(stopwords.words('english'))
    tokens = simple_preprocess(text, deacc=True)
    return [token for token in tokens if token not in stop_words]

def lda_topic_modeling_from_files(corpus_dir, output_dir):
    # Step 1: Read all text files
    file_names = []
    documents = []
    for fname in os.listdir(corpus_dir):
        if fname.endswith('.txt'):
            fpath = os.path.join(corpus_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    file_names.append(fname)
                    documents.append(content)

    # Step 2: Preprocess
    processed_docs = [preprocess(doc) for doc in documents]

    # Step 3: Create dictionary and BOW corpus
    dictionary = corpora.Dictionary(processed_docs)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    # Step 4: Train LDA model on all documents
    lda_model = models.LdaModel(
        corpus=bow_corpus,
        id2word=dictionary,
        num_topics=NUM_TOPICS,
        random_state=42,
        passes=10
    )

    # Step 5: Extract topic keywords
    topic_keywords = {}
    for topic_id in range(NUM_TOPICS):
        words = lda_model.show_topic(topic_id, topn=10)
        topic_keywords[str(topic_id)] = [word for word, _ in words]

    # Step 6: Process each document individually and write output
    for i, (fname, original_text, bow) in enumerate(zip(file_names, documents, bow_corpus)):
        topic_probs = lda_model.get_document_topics(bow)
        dominant_topic = max(topic_probs, key=lambda x: x[1])[0]

        doc_result = {
            'file_name': fname,
            'text': original_text,
            'dominant_topic': int(dominant_topic),
            'topic_distribution': {
                str(topic): float(prob) for topic, prob in topic_probs
            },
            'topic_keywords': topic_keywords  # Optional: remove if not needed
        }

        # Output file path
        output_file = os.path.join(output_dir, fname.replace('.txt', '_lda.json'))

        # Save result
        with open(output_file, 'w', encoding='utf-8') as f:
            print("now writing file:"+str(output_file))
            json.dump(doc_result, f, indent=4, ensure_ascii=False)

        print(f"✅ Saved result for '{fname}' → {output_file}")

# Run it
lda_topic_modeling_from_files(CORPUS_DIR, OUTPUT_DIR)
