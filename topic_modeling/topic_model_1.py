import nltk
import gensim
from gensim import corpora
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer

# Download stopwords if not already downloaded
nltk.download('stopwords')

# Your full text as a single string
text = """
Germany,[d] officially the Federal Republic of Germany,[e] is a country in Central Europe. It lies between the Baltic Sea and the North Sea to the north and the Alps to the south. Its sixteen constituent states have a total population of over 82 million, making it the most populous member state of the European Union. Germany borders Denmark to the north; Poland and the Czech Republic to the east; Austria and Switzerland to the south; and France, Luxembourg, Belgium, and the Netherlands to the west. The nation's capital and most populous city is Berlin and its main financial centre is Frankfurt; the largest urban area is the Ruhr. Settlement in the territory of modern Germany began in the Lower Paleolithic, with various tribes inhabiting it from the Neolithic onward, chiefly the Celts, with Germanic tribes inhabiting the north. Romans named the area Germania. In 962, the Kingdom of Germany formed the bulk of the Holy Roman Empire. During the 16th century, northern German regions became the centre of the Protestant Reformation. Following the Napoleonic Wars and the dissolution of the Holy Roman Empire in 1806, the German Confederation was formed in 1815. Unification of Germany into the modern nation-state, led by Prussia, established the German Empire in 1871. After World War I and a revolution, the Empire was replaced by the Weimar Republic. The Nazi rise to power in 1933 led to the establishment of a totalitarian dictatorship, World War II, and the Holocaust. In 1949, after the war and Allied occupation, Germany was organised into two separate polities with limited sovereignty: the Federal Republic of Germany (FRG), or West Germany, and the German Democratic Republic (GDR), or East Germany. The FRG was a founding member of the European Economic Community in 1951, while the GDR was a communist Eastern Bloc state and member of the Warsaw Pact. After the fall of the communist led-government in East Germany, German reunification saw the former East German states join the FRG on 3 October 1990. Germany is a developed country with a strong economy; it has the largest economy in Europe by nominal GDP. As a major force in several industrial, scientific and technological sectors, Germany is both the world's third-largest exporter and third-largest importer. Widely considered a great power, Germany is part of multiple international organisations and forums. It has the third-highest number of UNESCO World Heritage Sites: 55, of which 52 are cultural.
"""  # replace with your full text

# Remove all newlines
text = text.replace("\n", " ")

# Preprocessing
stop_words = set(stopwords.words('english'))
tokenizer = TreebankWordTokenizer()

def preprocess(text):
    tokens = tokenizer.tokenize(text.lower())               # tokenize and lowercase
    tokens = [word for word in tokens if word.isalpha()]    # keep only alphabetic tokens
    tokens = [word for word in tokens if word not in stop_words]  # remove stopwords
    return tokens

# Single document
texts = [preprocess(text)]

# Create dictionary and corpus
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(texts[0])]

# Build LDA model (5 topics)
lda_model = gensim.models.LdaModel(
    corpus,
    num_topics=2,
    id2word=dictionary,
    passes=15,
    random_state=42
)

# Print top words per topic
print("Top words per topic:")
for i, topic in lda_model.show_topics(num_topics=5, formatted=False):
    words = [word for word, prob in topic]
    print(f"Topic {i}: " + ", ".join(words))

# Print topic distribution for the single document
doc_topics = lda_model.get_document_topics(corpus[0])
sorted_topics = sorted(doc_topics, key=lambda x: x[1], reverse=True)
top_topic = sorted_topics[0][0] if sorted_topics else None
print(f"\nMain topic for the document: Topic {top_topic}")
