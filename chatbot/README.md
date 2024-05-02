
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







