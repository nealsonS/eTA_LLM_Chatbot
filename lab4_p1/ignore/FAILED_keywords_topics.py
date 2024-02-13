import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


def summarize(text, per):
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    #print(int(len(sentence_tokens)*per))
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    print(summary)
    return summary
    
  
  
article0 = """Sorry if this isnt the right subreddit for it but I needed to vent 

For the last yearish in the Android app I have been finding more and more bugs crashes functionality not working and other bits of functionality that should have been implemented years ago for improvements in user life experience

Doing a quick check on their website it looks like there are no job openings which makes me think that they are just working with a software skeleton crew and wont be making any big fixes anytime soon and things can only go downhill from here

Edit Good to see Im not the only one who feels the same about the app FYI I was in the top 3 users last year
I wont post a list of bugs Mainly because if a multimillion company wants to improve their product they should hire talent instead of spending money on corporate payouts stock buybacks or other similar practices to instead increase the value of the company

And if you havent found any bug good for you"""


article1 = """Sorry if this isnt the right subreddit for it but I needed to vent For the last yearish in the Android app I have been finding more and more bugs crashes functionality not working and other bits of functionality that should have been implemented years ago for improvements in user life experience Doing a quick check on their website it looks like there are no job openings which makes me think that they are just working with a software skeleton crew and wont be making any big fixes anytime soon and things can only go downhill from here Edit Good to see Im not the only one who feels the same about the app FYI I was in the top 3 users last year I wont post a list of bugs Mainly because if a multimillion company wants to improve their product they should hire talent instead of spending money on corporate payouts stock buybacks or other similar practices to instead increase the value of the company And if you havent found any bug good for you"""
# same result as the above

article2 = "28-ton, 1.2-megawatt tidal kite is now exporting power to the grid"
# not good, can't do less than 1.0, which is basically the entire sentence

summarize(article2, 0.99)
