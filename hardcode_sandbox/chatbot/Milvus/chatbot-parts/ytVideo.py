from youtube_transcript_api import YouTubeTranscriptApi as yta


def print_time():
	return "print_time imported"


def search_for_word():
	message = print_time(), "search_for_word imported"
	return message


def yt_time():
	message = search_for_word(), "yt_time imported"
	return message
	

def print_time_real(search_word, time, video_id):
	# calculate the accurate time according to the video's duration
	for t in time:
		hours = int(t // 3600)
		mins = int((t // 60) % 60)
		secs = int(t % 60)
		time_stamp = f"{hours:02d}:{mins:02d}:{secs:02d}"
		l_hours, l_mins, l_secs = map(int, time_stamp.split(':'))
		formatted_time_stamp = f"{l_hours}h{l_mins}m{l_secs}s"
	print(f"\nVideo:\n'{search_word}' was mentioned at: \nhttps://www.youtube.com/watch?v={video_id}&t={formatted_time_stamp}\n{hours:02d}:{mins:02d}:{secs:02d}")


def search_for_word_real(search_word, transcript, data, video_id):
	time = []
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
		time.append(final_time)
	if len(time) == 0:
		return False
		#print("Word not found in the source video.")=
	else:
		print_time(search_word, time, video_id) #and the video link
		return True


def yt_time_real(video_id, search_word):
	transcript = yta.get_transcript(video_id, languages=('us', 'en')) 
	data = [t['text'] for t in transcript]
	data = [re.sub(r"[^a-zA-Z0–9-ışğöüçiIŞĞÖÜÇİ ]", "", line) for line in data]
	return search_for_word(search_word, transcript, data, video_id)
