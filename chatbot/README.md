*NOTE TO TEAM*: Additional materials on Google Drive: https://drive.google.com/drive/folders/104F88GdLSjuGbi7pKkPo7mHvDKDiIlbI?usp=drive_link 


####### TO DO (part 1): ########
- scrape data from links in "websites_to_scrape.txt", PDFs in raw_course_materials and put into database
- train and save LLM with current data
- make a prototype website / app for chatbot to start answering questions based on current LLM model



Make sure to do the following first:
### Installations:
- pip install piazza-api #for piazza
- pip install html2text 
- pip install youtube-transcript-api #for YT video transcription + time
- pip install -U stable-ts   #for video transcription and time
- pip install -U git+https://github.com/jianfch/stable-ts.git  #for video transcription and time
- pip install accelerate  #for video transcription and time with HuggingFace 
- pip install transformers accelerate optimum  #for video transcription and time with HuggingFace


### Course Materials
Primary: NIH Principles of Clinical Pharmacology Course Materials

Secondary: MIT OpenCourseWare Principles of Pharmacology

There are currently no lecture videos in the local machine, but the videos we will be using are available here: https://www.youtube.com/playlist?list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt

Textbook: Arthur J. Atkinson Jr., Shiew-Mei Huang, Juan J.L. Lertora, Sanford P. Markey - Principles of Clinical Pharmacology, Third Edition-Academic Press (2012)
*Note:* textbook is optional in NIH course

Supplemental Textbook (older version required by MIT course, but this is newer): David E. Golan MD PhD - Principles of Pharmacology_ The Pathophysiologic Basis of Drug Therapy-LWW (2016)

Syllabus: copy of NIH's 2023-2024 syllabus


### Video & Transcription
Contains codes for video
 
## frame_extractor.py
Input local MP4 file.
Output JPG files of video frames.


## text_extractor.py
Input local MP4 file.
Output WAV file, TXT file for transcription.


## yt_extractor.py
Input YouTube link and search term.
Output time stamps of all the times the transcribed search term appears.
If we can get this to get video frames, we can avoid downloading lecture videos into local machine.
The only caveat is that instructors would have to upload their lectures onto YouTube. 
*Issues:* 
A. currently time stamps are ahead by 2-3 seconds.


## openai_whisper.py
Input MP3 or WAV file.
Output SRT file with time stamps of phrases of words.
To be used when Chatbot needs to reference a letter.
*Issues:* 
A. have not checked with source video if time stamps are correct. 
B. huggingface transformer is supposed to be faster, but it is not faster and not as accurate for some reason.
C. faster_whisper should be available but is missing installed package, will need to find it to test its performance.



### Piazza
Contains code to connect with Piazza

## fetch_post.py
Input valid Piazza email, pw and course.
Output TXT file of posts from course.
Goal of using this is to collect more data to train Chatbot on Pharmacology student questions.
Maybe also to post on Piazza as Chatbot replies to students?
*Issues:*
A. will only work for existing Piazza courses? Pharmacology does not seem to have a course on Piazza, that I know of.



### LLM
Currently uses Lab 6's OpenAI for LLM (do 'nano .env' to find OpenAI key.

## pdf_extractor.py
Input folder path with PDFs. (sample one: /home/eTA_LLM_Chatbot/chatbot/raw_course_materials)
Output extracted data into MySQL database and images into images folder (might remove images feature in the future)



