from gensim.models import CoherenceModel
#from get_mysql_data import get_dataset_from_mysql
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



def gensim_topic_clustering2(documents, optimal_topics):
    processed_docs = [preprocess_text(doc) for doc in documents]
    # create dictionary and corpus
    dictionary = corpora.Dictionary(processed_docs)
    corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
    # train LDA model
    num_topics = optimal_topics
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)
    for topic_id, topic_words in lda_model.print_topics():
    	# only get the words, not probability
        words = [word.split("*")[1].replace('"', '') for word in topic_words.split(" + ")]
        print(f"\nTopic #{topic_id + 1}: {', '.join(words)}")
        # store documents under each topic
        topic_docs = []
        for i in range(len(corpus)):
            model = sorted(enumerate(lda_model.get_document_topics(corpus[i])), key=lambda x: x[1][1], reverse=True)
            for index, (doc_topic_id, probability) in model:
                if doc_topic_id == topic_id:
                    topic_doc = {'topic_id': doc_topic_id, 'probability': probability, 'document': documents[i]}
                    topic_docs.append(topic_doc)
                    break  # break after finding the topic in the document
        # Print documents for the current topic
        sorted_topic_docs = sorted(topic_docs, key=lambda x: x['probability'], reverse=True)
        for t in sorted_topic_docs:
            print(f"{t['topic_id']+1}\t{t['probability']:.4f}\t{t['document'][:70]}")

    vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary=lda_model.id2word, sort_topics=False)
    pyLDAvis.save_html(vis, 'tech_clusters.html')
    #display(HTML('tech_clusters.html'))
    print("Please open 'tech_clusters.html' to view the visualization.")
    

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

    # visualize coherence scores
    import matplotlib.pyplot as plt
    x = range(start, limit + 1, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence Score")
    plt.show()

    optimal_num_topics = start + coherence_values.index(max(coherence_values)) * step
    return optimal_num_topics


def optnumtop():
    print('Retrieving Data from MySQL\n')
    df, con = get_dataset_from_mysql()
    content = df.loc[:, 'content']
    documents = content
    # find optimal number of topics before doing LDA
    optimal_topics = find_optimal_number_of_topics(documents)
    print(f"The optimal number of topics is: {optimal_topics}")
    gensim_topic_clustering2(documents, optimal_topics)


