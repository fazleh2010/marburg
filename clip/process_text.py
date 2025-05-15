import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK resources
nltk.data.path.append("/home/melahi/code/image-data/nltk_data/")  # Ensure NLTK finds its data
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
print(nltk.data.path)


# Load your text file
path="/home/melahi/code/image-data/test/"
file_name="text.txt"

with open(path+file_name, 'r', encoding='utf-8') as f:
    raw_text = f.read()

# Split the text into smaller documents (e.g., by paragraph or sentence)
documents = raw_text.split('\n')  # or use `nltk.sent_tokenize(raw_text)` for sentence-wise

# Preprocess each document
stop_words = set(stopwords.words('english'))
texts = [
    [word.lower() for word in word_tokenize(doc) if word.isalpha() and word.lower() not in stop_words]
    for doc in documents if doc.strip() != ''
]
