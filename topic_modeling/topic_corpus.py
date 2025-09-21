import os
import json
import nltk
from gensim import corpora, models
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from langdetect import detect  # lightweight language detector

# Ensure stopwords are downloaded
nltk.download('stopwords')

# Parameters
CORPUS_DIR = '/home/melahi/code/marburg/documents/corpus_texts'
OUTPUT_DIR = '/home/melahi/code/marburg/documents/lda_per_file_output'
NUM_TOPICS = 3

# Make sure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Preprocessing function with dynamic language
def preprocess(text, lang):
    try:
        stop_words = set(stopwords.words(lang))
    except OSError:
        # fallback if stopwords not available
        stop_words = set(stopwords.words('english'))
    tokens = simple_preprocess(text, deacc=True)  # Remove punctuations
    return [token for token in tokens if token not in stop_words]

# Main function to run LDA per file
def lda_topic_modeling_from_files(corpus_dir, output_dir):
    file_names = []
    documents = []
    languages = []

    # Step 1: Read and detect language
    for fname in os.listdir(corpus_dir):
        if fname.endswith('.txt'):
            fpath = os.path.join(corpus_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:  # Skip empty files
                    file_names.append(fname)
                    documents.append(content)
                    try:
                        lang = detect(content)
                    except:
                        lang = 'english'  # fallback
                    languages.append(lang)

    # Step 2: Preprocess docs based on detected language
    processed_docs = [preprocess(doc, lang) for doc, lang in zip(documents, languages)]

    # Step 3: Create dictionary and BOW corpus
    dictionary = corpora.Dictionary(processed_docs)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    # Step 4: Train LDA model
    lda_model = models.LdaModel(
        corpus=bow_corpus,
        id2word=dictionary,
        num_topics=NUM_TOPICS,
        random_state=42,
        passes=10
    )

    # Step 5: Extract top keywords per topic
    topic_keywords = {
        str(topic_id): [word for word, _ in lda_model.show_topic(topic_id, topn=10)]
        for topic_id in range(NUM_TOPICS)
    }

    # Step 6: Evaluate each document
    for i, (fname, original_text, bow, lang) in enumerate(zip(file_names, documents, bow_corpus, languages)):
        topic_probs = lda_model.get_document_topics(bow)
        dominant_topic = max(topic_probs, key=lambda x: x[1])[0]

        result = {
            'file_name': fname,
            'language': lang,
            'text': original_text,
            'dominant_topic': int(dominant_topic),
            'topic_distribution': {str(topic): float(prob) for topic, prob in topic_probs},
            'topic_keywords': topic_keywords
        }

        output_file = os.path.join(output_dir, fname.replace('.txt', '_lda.json'))

        # Write output to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            print("📝 Writing:", output_file)
            json.dump(result, f, indent=4, ensure_ascii=False)

        print(f"✅ Done with '{fname}' → {output_file}")

# Run the function
if __name__ == '__main__':
    lda_topic_modeling_from_files(CORPUS_DIR, OUTPUT_DIR)
