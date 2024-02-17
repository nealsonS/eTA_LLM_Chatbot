from gensim.models import CoherenceModel
from get_mysql_data import get_dataset_from_mysql
from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
from nltk.tokenize import word_tokenize
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
from IPython.core.display import HTML
from IPython.core.display import display


def is_single_char(s):
    return len(s) == 1


def preprocess_text(text):
    # tokenize and remove stopwords
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in STOPWORDS]
    #music_stop= ['music', 'like', 'likes', 's', 'im', 'ive']
    #math_stop = ['math', 'mathematics', 'like', 'likes', 's', 'im', 'ive']
    tech_stop = ['tech', 'technology', 'like', 'likes', 'research', 'researchers', 'teams', 'team', 'im', 'said', 'study', 'ive', 'new', 'university', 'says', 'use', 'material', 'materials']
    tokens = [word.lower() for word in tokens if word.lower() not in tech_stop and not word.lower().isdigit() and not is_single_char(word)] #checks for numbers and single-char words
    return tokens



def gensim_topic_clustering(documents, optimal_topics):
    processed_docs = [preprocess_text(doc) for doc in documents]

    # create dictionary and corpus
    dictionary = corpora.Dictionary(processed_docs)
    corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    # train LDA model
    num_topics = optimal_topics
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

   # display topics and associated documents
    for topic_id, topic_words in lda_model.print_topics():
        # extracting only words from topic words
        words = [word.split("*")[1].replace('"', '') for word in topic_words.split(" + ")]
        print(f"\nTopic #{topic_id + 1}: {', '.join(words)}")
   
   # will fix this to show documents under topics
#    topic_docs = [document for document, score in sorted(enumerate(lda_model.get_document_topics(corpus[0])), key=lambda x: -x[1][topic_id])]
 #   if topic_docs:
        # print first few documents in the cluster
  #      for doc_index in topic_docs[:5]:
   #         print(f"Document #{doc_index + 1}: {documents[0][:50]}...")  
   # else:
    #    print("No documents in this cluster.")


        
    # visualize topics with pyLDAvis (makes a separate html file in the folder, open that to view visualization)
    vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary=lda_model.id2word)
    pyLDAvis.save_html(vis, 'lda_result_tech_opt.html')
    display(HTML('lda_result_tech_opt.html'))
    
    

def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=1):
    coherence_values = []
    model_list = []
    
    for num_topics in range(start, limit + 1, step):
        model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)
        model_list.append(model)
        coherence_model = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherence_model.get_coherence())

    return model_list, coherence_values


def find_optimal_number_of_topics(documents, start=2, limit=10, step=1):
    processed_docs = [preprocess_text(doc) for doc in documents]
    dictionary = corpora.Dictionary(processed_docs)
    corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    model_list, coherence_values = compute_coherence_values(dictionary, corpus, processed_docs, limit, start, step)

    # Plot the coherence scores
    import matplotlib.pyplot as plt
    x = range(start, limit + 1, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence Score")
    plt.show()

    # Find the optimal number of topics with the highest coherence score
    optimal_num_topics = start + coherence_values.index(max(coherence_values)) * step
    return optimal_num_topics


if __name__ == '__main__':
    print('Retrieving Data from MySQL\n')
    df, con = get_dataset_from_mysql()
    content = df.loc[:, 'content']

    documents = content

    # Find the optimal number of topics
    #optimal_topics = find_optimal_number_of_topics(documents)
    #print(f"The optimal number of topics is: {optimal_topics}")

    # Use the optimal number of topics in your LDA model
    gensim_topic_clustering(documents, 5)#optimal_topics)

