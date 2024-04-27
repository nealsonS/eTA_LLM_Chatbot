

def word_in_doc(word_to_find, source_text):
	word_index = source_text.find(word_to_find)
	# if word found
	if word_index != -1:
		# start and end indices for substring
		start_index = max(0, word_index - 100)
		end_index = min(len(source_text), word_index + len(word_to_find) + 100)
		# extract substring
		output_string = source_text[start_index:end_index]
		output_string = output_string.replace(word_to_find, "\033[1m\033[3m\033[4m"+word_to_find+"\033[0m")
		#print('\nText Excerpt:\n"'+ output_string + '"')
		return True, output_string
	else:
		output_string = "No references in notes"
		return False, output_string
