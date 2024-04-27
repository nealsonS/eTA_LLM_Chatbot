from rake_nltk import Rake
import nltk
nltk.download('stopwords')
nltk.download('punkt')


def find_keywords(query):
	rake_nltk_var = Rake()
	rake_nltk_var.extract_keywords_from_text(query)
	keyword_extracted = rake_nltk_var.get_ranked_phrases()
	return(keyword_extracted)

