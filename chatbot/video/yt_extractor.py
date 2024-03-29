# code from https://medium.com/@oladenj/extracting-timestamps-from-youtube-video-transcripts-using-python-e2329503d1e0
# this is to avoid downloading videos to local machine. But would then require lecture videos to be uploaded to YT...


from youtube_transcript_api import YouTubeTranscriptApi as yta
import re


def print_time(search_word,time):
    print(f"'{search_word}' was mentioned at:")
    # calculate the accurate time according to the video's duration
    for t in time:
        hours = int(t // 3600)
        min = int((t // 60) % 60)
        sec = int(t % 60)
        print(f"{hours:02d}:{min:02d}:{sec:02d}")
        
        
def yt_link_to_id(video_link):   
    regex = re.compile(r'^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/|shorts\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*')
    match = regex.match(video_link)
    if match:
        #print(match.group(1))
        return match.group(1)


if __name__=="__main__":
    #video link: https://www.youtube.com/watch?v=ArFQdvF8vDE
    video_link = input("Enter YouTube video link:\n")
    video_id = yt_link_to_id(video_link)  
    #print(video_id)
    #video_id = "ArFQdvF8vDE"
    transcript = yta.get_transcript(video_id, languages=('us', 'en'))

    data = [t['text'] for t in transcript]
    data = [re.sub(r"[^a-zA-Z0–9-ışğöüçiIŞĞÖÜÇİ ]", "", line) for line in data]
    search_word = input("What word are you looking for?\n")
    time = []
    for i, line in enumerate(data):
        if search_word in line:
            start_time = transcript[i]['start']
            time.append(start_time)
    print_time(search_word, time)

