## automated_yt_extractor.py
Combines former YouTube video transcription to get transcriptions of all videos in NIH playlist (`https://www.youtube.com/playlist?list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt`) into PDF format.
1. Inputs video source
2. Outputs PDF file of transcripts (can be found in `../all_course_materials`)

 
## yt_extractor.py
Precursor to `combined_video_transcription.py`.
1. Input YouTube link and search term
2. Output time stamps of all the times the transcribed search term appears


## text_extractor.py
Precursor to `combined_video_transcription.py`.
1. Input local MP4 file
2. Outputs WAV file (only audio of MP4)
3. Inputs WAV file
4. Output transcription of WAV file into TXT file


## combined_video_transcription.py 
Combines YouTube video transcription with timestamp code and  MP4 --> WAV transcription code. <br>
Precursor to `../chatbotParts/ytVideo.py`.
1. Inputs user desired mode and video source
2. Outputs timestamps for searched word
