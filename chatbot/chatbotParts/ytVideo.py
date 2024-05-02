from youtube_transcript_api import YouTubeTranscriptApi as yta
import re
import math



def search_for_word(search_word, transcript, data, video_id):
	final_time = 0
	for i, line in enumerate(data):
		words = re.findall(r'\b\w+\b', line)  # split line into words for more accurate searching, rather than if word is a subset of the line
		if search_word in words:
			#print(line) 
			start_time = transcript[i]['start']
			# to accomodate for start time not being the actual word
		text = re.sub(r"(?<=:)([A-Z]+)", "", line).split(' ') # remove stuff like: 'AUDIENCE: '
		try:
			i_word = text.index(search_word) + 1
		except ValueError:
			continue  
		added_time = (i_word / len(text)) * transcript[i]['duration']
		#print(added_time) 
		final_time = start_time + added_time
		#print(final_time)
		#time.append(final_time)
	if final_time == 0:
		return False, 0
		#print("Word not found in the source video.")
	else:
		timestamp = int(final_time)#find_time(search_word, time, video_id) #and the video link
		return True, timestamp


def yt_time(video_id, search_word):
	transcript = yta.get_transcript(video_id, languages=('us', 'en')) 
	data = [t['text'] for t in transcript]
	data = [re.sub(r"[^a-zA-Z0–9-ışğöüçiIŞĞÖÜÇİ ]", "", line) for line in data]
	return search_for_word(search_word, transcript, data, video_id)
