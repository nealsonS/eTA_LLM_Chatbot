from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
from nltk.tokenize import word_tokenize
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
from IPython.core.display import HTML
from IPython.core.display import display
from get_mysql_data import get_dataset_from_mysql



def preprocess_text(text):
    # tokenize and remove stopwords
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in STOPWORDS]
    return tokens



def gensim_topic_clustering(documents):
    processed_docs = [preprocess_text(doc) for doc in documents]

    # create dictionary and corpus
    dictionary = corpora.Dictionary(processed_docs)
    corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    # train LDA model
    num_topics = 5 
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

    # display topics
    for topic_id, topic_words in lda_model.print_topics():
        print(f"Topic #{topic_id + 1}: {topic_words}")
        
    # visualize topics with pyLDAvis (makes a separate html file in the folder, open that to view visualization)
    vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary=lda_model.id2word)
    pyLDAvis.save_html(vis, 'lda_result.html')
    display(HTML('lda_result.html'))
    



if __name__ == '__main__':
    print('Retrieving Data from MySQL\n')
    df, con = get_dataset_from_mysql()
    content = df.loc[:, 'content']

    documents = content

    gensim_topic_clustering(documents)

