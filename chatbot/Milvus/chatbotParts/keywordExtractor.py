from rake_nltk import Rake
import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)


def find_keywords(query):
	rake_nltk_var = Rake()
	rake_nltk_var.extract_keywords_from_text(query)
	keyword_extracted = rake_nltk_var.get_ranked_phrases()
	return(keyword_extracted)

