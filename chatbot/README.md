*NOTE TO TEAM*: Additional materials on Google Drive: https://drive.google.com/drive/folders/104F88GdLSjuGbi7pKkPo7mHvDKDiIlbI?usp=drive_link 


Make sure to do the following first:
### Installations:
- pip install html2text 
- pip install youtube-transcript-api #for YT video transcription + time
- pip install -U stable-ts   #for video transcription and time
- pip install -U git+https://github.com/jianfch/stable-ts.git  #for video transcription and time
- pip install accelerate  #for video transcription and time with HuggingFace 
- pip install transformers accelerate optimum  #for video transcription and time with HuggingFace




### React (in 'chatbot-react' folder)
Our chatbot runs on React




### Milvus (in 'Milvus' folder)
Database that stores embeddings. 
!!! NEED TO REDO EMBEDDINGS WITH BIOLOGY FORUM TEXT

## rag_res.py
Inputs user questions, one at the time.
Outputs AI-generated response (HuggingFace embeddings with OpenAI), and applicable video timestamp and lecture notes excerpt and page.


## argument_rag_res.py
Similar to rag_res.py, except it only takes user input once when running. 
Please enter `python3 argument_rag_res.py {question}` when running the script. 
For testing integration with React codes


## convo_memory.py
Testing conversation memory of chatbot.




### LLM (in 'llm' folder)
Currently uses Lab 6's OpenAI for LLM (do 'nano .env' to find OpenAI key.

## huggingface_embeddings (folder)
Different scripts to test performance of Huggingface embeddings. These were not reused in final version

## openai_cookbook (folder)
Different scripts to test performance of OpenAI embeddings. This method was not reused in final version



### Course Materials (organized in 'organized_course_materials' folder and all together in 'all_course_materials' folder)
Primary: NIH Principles of Clinical Pharmacology Course Materials

Secondary: MIT OpenCourseWare Principles of Pharmacology

There are currently no lecture videos in the local machine, but the videos we will be using are available here: `https://www.youtube.com/playlist?list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt`
The transcripts of these videos are in PDF format so that our PDF reader can scrape the data.

Textbook: Arthur J. Atkinson Jr., Shiew-Mei Huang, Juan J.L. Lertora, Sanford P. Markey - Principles of Clinical Pharmacology, Third Edition-Academic Press (2012)
*Note:* textbook is optional in NIH course

Supplemental Textbook (older version required by MIT course, but this is newer): David E. Golan MD PhD - Principles of Pharmacology_ The Pathophysiologic Basis of Drug Therapy-LWW (2016)

Syllabus: copy of NIH's 2023-2024 syllabus

Wikipedia of Pharmacology and related page links

Forum: Biology Forum - Pharmacology




### Video & Transcription (in 'video' folder)
Contains codes for video. Most were testing different potential features.
 
## automated_yt_extractor.py
Combines former YouTube video transcription to get transcriptions of all playlist videos into PDF format.
Inputs video source
Outputs PDF file of transcripts
*Note:* 
A. It can handle the longest video in the NIH YT playlist, which is 1:29:55: https://www.youtube.com/watch?v=6efVpOoBjiw&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=15 
B. the PDF outputs are found in the course materials folders

 
## frame_extractor.py
Input local MP4 file.
Output JPG files of video frames.


## yt_extractor.py
Input YouTube link and search term.
Output time stamps of all the times the transcribed search term appears.
If we can get this to get video frames, we can avoid downloading lecture videos into local machine.
The only caveat is that instructors would have to upload their lectures onto YouTube. 
*Note:* code reused in other scripts


## all_video_transcription.py (discontinued)
Combines former YouTube video transcription + timestamp code with former MP4-->WAV transcription code.
Inputs user desired mode and video source
Outputs timestamps for searched word
*Note:* 
A. It can handle the longest video in the NIH YT playlist, which is 1:29:55: https://www.youtube.com/watch?v=6efVpOoBjiw&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=15 
B. Currently having issues on the MP4 transcription. Since we are not using MP4 videos, we have decided to scrap this code.
 

## text_extractor.py (discontinued)
Input local MP4 file.
Output WAV file, TXT file for transcription.
*Note:* Will not be used


## openai_whisper.py (discontinued)
Input MP3 or WAV file.
Output SRT file with time stamps of phrases of words.
To be used when Chatbot needs to reference a letter.
*Issues:* 
A. have not checked with source video if time stamps are correct. 
B. huggingface transformer is supposed to be faster, but it is not faster and not as accurate for some reason.
C. faster_whisper should be available but is missing installed package, will need to find it to test its performance.




### Webscraping (in 'webscraping' folder)
Different scripts to scrape data from Biology Forum, Wikipedia, etc.
