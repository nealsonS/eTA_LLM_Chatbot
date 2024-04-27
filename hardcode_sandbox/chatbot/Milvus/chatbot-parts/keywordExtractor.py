from rake_nltk import Rake
import nltk
nltk.download('stopwords')
nltk.download('punkt')



def find_keywords():
	return "find_keywords imported"


def find_keywords_real(query):
	rake_nltk_var = Rake()
	query = """spaCy is an open-source software library for advanced natural language processing, written in the programming languages Python and Cython. The library is published under the MIT license and its main developers are Matthew Honnibal and Ines Montani, the founders of the software company Explosion."""
	rake_nltk_var.extract_keywords_from_text(query)
	keyword_extracted = rake_nltk_var.get_ranked_phrases()
	#print(keyword_extracted)
	#print(type(keyword_extracted))
	return(keyword_extracted)

