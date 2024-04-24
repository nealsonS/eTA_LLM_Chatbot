# this is to avoid downloading videos to local machine. But would then require lecture videos to be uploaded to YT...
# will require this code to be in the same folder as the code?


from youtube_transcript_api import YouTubeTranscriptApi as yta
import re
## for MP4 --> transcription
import speech_recognition as sr
from pydub import AudioSegment
import os
## for audio duration
import librosa
## for vosk
#import wave
#import json
#from vosk import Model, KaldiRecognizer, SetLogLevel
import Word as custom_Word
import vosk_transcription


## make something that will clear pycache folder??

def audio_transcriber(name_file):
    r = sr.Recognizer()
    # Open the audio file
    with sr.AudioFile(name_file) as source:
        audio_text = r.record(source)
    # Recognize the speech in the audio
    text = r.recognize_google(audio_text) #requires online connection
    duration = librosa.get_duration(path=name_file)
    transcipt = [{'text': text, 'start': 0.00, 'duration': duration}]
    return transcipt



def mp4_transcriber(name_file):
    video = AudioSegment.from_file(name_file, format="mp4")
    audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    audio_name_file = name_file.replace("mp4", "wav") #need to account for MP4
    audio.export(audio_name_file, format="wav")
    # initialize recognizer class (for recognizing the speech)
    transcript = []
    
    # vosk attempt -- unfortunately, keeps using too much memory...
    #list_of_Words = vosk_transcription.audio_transcriber(audio_name_file)
    #transcipt = [{'text': text, 'start': 0.00, 'duration': duration}]
    #for word in list_of_Words:
    #    transcript.append({'text': word.text, 'start': word.start, 'duration': word.duration})
    print(list_of_Words)



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
    
    
def yt_video():
    #video link: https://www.youtube.com/watch?v=ArFQdvF8vDE
    video_link = input("Enter YouTube video link:\n")
    video_id = yt_link_to_id(video_link)  
    #print(video_id)
    #video_id = "ArFQdvF8vDE"
    transcript = yta.get_transcript(video_id, languages=('us', 'en')) 
    return transcript
    
    
def search_word():
    search_word = input("What word are you looking for?\n")
    time = []
    for i, line in enumerate(data):
        words = re.findall(r'\b\w+\b', line)  # split line into words for more accurate searching, rather than if word is a subset of the line
        if search_word in words:
            print(line)
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
        print("Word not found.")
    else:
        print_time(search_word, time)


if __name__=="__main__":
    mode = input("1. YouTube video \n2. Local MP4 \n3. Local WAV\n")
    #transcript = []
    if mode == "1":
        transcript = yt_video()
    elif mode == "2":
        name_file = input("Name of file:\n")
        mp4_transcriber(name_file) 
        #transcript = mp4_transcriber(name_file) #needs to be in the same format as yta
        #print(transcript)
    elif mode == "3":
        name_file = input("Name of file:\n")
        transcript = audio_transcriber(name_file)  #needs to be in the same format as yta
#    data = [t['text'] for t in transcript]
#    data = [re.sub(r"[^a-zA-Z0–9-ışğöüçiIŞĞÖÜÇİ ]", "", line) for line in data]
#    print(data)
#    option = input("\nSearch for word and its timestamp(s)? Y/N\n")
#    if option.lower() == 'y':
#        search_word()


