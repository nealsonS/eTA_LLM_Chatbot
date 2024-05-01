from youtube_transcript_api import YouTubeTranscriptApi as yta
import re
import os
from fpdf import FPDF
 
 
 
def text_to_pdf(transcript_list, num, video_id):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 11)
    pdf.cell(200, 10, txt = str(num), ln = 1, align = 'C')
    for t in range(len(transcript_list)):
        pdf.cell(200, 10, txt = transcript_list[t], ln = t, align = 'C')
    filename = 'ytvid_' + str(num) + '_' + video_id + '.pdf'
    pdf.output(filename)   



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
    
    
def yt_video(video_link):
    #video link: https://www.youtube.com/watch?v=ArFQdvF8vDE
    #video_link = input("Enter YouTube video link:\n")    
    video_id = yt_link_to_id(video_link)  
    #print(video_id)
    #video_id = "ArFQdvF8vDE"
    transcript = yta.get_transcript(video_id, languages=('us', 'en')) 
    return transcript, video_id
    
    
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
    urls = [
    'https://www.youtube.com/watch?v=47QLbE3D9gg&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=1',
    'https://www.youtube.com/watch?v=4AHbHaQmGm8&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=2',
    'https://www.youtube.com/watch?v=3vWD5fG4TCo&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=3',
    'https://www.youtube.com/watch?v=ECEJrTjwgNw&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=4',
    'https://www.youtube.com/watch?v=B9wnHsRewYE&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=5',
    'https://www.youtube.com/watch?v=IT6eHxvAjcQ&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=6',
    'https://www.youtube.com/watch?v=uzobez8W1yI&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=7',
    'https://www.youtube.com/watch?v=DJX3hsvbSrI&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=8',
    'https://www.youtube.com/watch?v=QGh6AQXXMi0&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=9',
    'https://www.youtube.com/watch?v=bqKHy2xeIkw&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=10',
    'https://www.youtube.com/watch?v=Q79HYq-fFmY&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=11',
    'https://www.youtube.com/watch?v=7u0yZaeE0GU&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=12',
    'https://www.youtube.com/watch?v=TozOUOj2YvI&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=13',
    'https://www.youtube.com/watch?v=8SjxRWwqMkQ&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=14',
    'https://www.youtube.com/watch?v=6efVpOoBjiw&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=15',
    'https://www.youtube.com/watch?v=HzeICXXGB-Q&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=16',
    'https://www.youtube.com/watch?v=leo3GOiJz5I&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=17',
    'https://www.youtube.com/watch?v=s_NM-MJa4Bo&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=18',
    'https://www.youtube.com/watch?v=5XxF0yPEvRQ&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=19',
    'https://www.youtube.com/watch?v=bcC6YRSm7Q8&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=20',
    'https://www.youtube.com/watch?v=5FHS8wcvMN0&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=21',
    'https://www.youtube.com/watch?v=T8ULhdTt4kY&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=22',
    'https://www.youtube.com/watch?v=agFA8z0f3eU&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=23',
    'https://www.youtube.com/watch?v=WaLVjoAA2lE&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=24',
    'https://www.youtube.com/watch?v=ij65dfo34K0&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=25',
    'https://www.youtube.com/watch?v=kVLoszELVP4&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=26',
    'https://www.youtube.com/watch?v=scawkYOZOF8&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=27',
    'https://www.youtube.com/watch?v=uBSldOMSMsg&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=28',
    'https://www.youtube.com/watch?v=NchhDVZHGKs&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=29',
    'https://www.youtube.com/watch?v=icWnjO0IWUE&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=30',
    'https://www.youtube.com/watch?v=P0AQ_VndPG8&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=31',
    'https://www.youtube.com/watch?v=X2-JTuSLuvQ&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=32',
    'https://www.youtube.com/watch?v=nxLxgRyaXks&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=33',
    'https://www.youtube.com/watch?v=0hfyMV69oCU&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=34',
    'https://www.youtube.com/watch?v=cCY9jY_H5OE&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=35',
    'https://www.youtube.com/watch?v=KB7Ct6vdIGI&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=36',
    'https://www.youtube.com/watch?v=LjsuCafsSR0&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=37',
    'https://www.youtube.com/watch?v=EiG0rYmLnKA&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=38',
    'https://www.youtube.com/watch?v=KGKmYmcOZHY&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=39',
    'https://www.youtube.com/watch?v=yK3EdNZMDAc&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=40',
    'https://www.youtube.com/watch?v=tpuKzBdIE2c&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=41',
    'https://www.youtube.com/watch?v=hYl9xtEUC-o&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=42',
    'https://www.youtube.com/watch?v=cJXC3kc91jM&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=43',
    'https://www.youtube.com/watch?v=oSm8Oglkg5Y&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=44',
    'https://www.youtube.com/watch?v=1qvfSMJJpQU&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=45',
    'https://www.youtube.com/watch?v=CaWK2M7Opvw&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=46',
    'https://www.youtube.com/watch?v=vy2r6xYY0do&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=47',
    'https://www.youtube.com/watch?v=Qxg3toMvcSQ&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=48',
    'https://www.youtube.com/watch?v=9uzsdWfnBLA&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=49',
    'https://www.youtube.com/watch?v=BXLo5dkP6Rs&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=50',
    'https://www.youtube.com/watch?v=7GWAx1BPoFI&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=51',
    'https://www.youtube.com/watch?v=8grNpPkA5PA&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=52',
    'https://www.youtube.com/watch?v=1PBrjhceJ9w&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=53',
    'https://www.youtube.com/watch?v=uUOv_wfL3ns&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=54',
    'https://www.youtube.com/watch?v=IFGcMrOHlVk&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=55',
    'https://www.youtube.com/watch?v=zqLkBeGp8g8&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=56',
    'https://www.youtube.com/watch?v=WxBbNt3C-Lg&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=57',
    'https://www.youtube.com/watch?v=6Vm9qRDAVpM&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=58',
    'https://www.youtube.com/watch?v=VUXpWGXyPZY&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=59',
    'https://www.youtube.com/watch?v=PmBBWK5RiQw&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=60',
    'https://www.youtube.com/watch?v=ApigSqhiO4c&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=61',
    'https://www.youtube.com/watch?v=kOmBvOZBhAU&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=62',
    'https://www.youtube.com/watch?v=KcRD15GvSPY&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=63',
    'https://www.youtube.com/watch?v=Zbr-S2H-mWY&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=64',
    'https://www.youtube.com/watch?v=22Dcc7A1tFA&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=65',
    'https://www.youtube.com/watch?v=jJhF_kQoJAs&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=66',
    'https://www.youtube.com/watch?v=C71XRb_zmB8&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=67',
    'https://www.youtube.com/watch?v=nP7bcN16-hI&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=68',
    'https://www.youtube.com/watch?v=Hz4Bk_EExaQ&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=69',
    'https://www.youtube.com/watch?v=2QDXo0flSEs&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=70',
    'https://www.youtube.com/watch?v=nlRs_uJZP4w&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=71',
    'https://www.youtube.com/watch?v=-1oCmCQABNM&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=72',
    'https://www.youtube.com/watch?v=MJqACCWeCHg&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=73',
    'https://www.youtube.com/watch?v=VfmqgsEfGtM&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=74',
    'https://www.youtube.com/watch?v=ZdT-mhRdjUk&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=75',
    'https://www.youtube.com/watch?v=FWCgcVc0Fx0&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=76',
    'https://www.youtube.com/watch?v=Fj0oNf5k_o8&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=77',
    'https://www.youtube.com/watch?v=8rnQZOXBkr8&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=78',
    'https://www.youtube.com/watch?v=j5coiHSLCSo&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=79',
    'https://www.youtube.com/watch?v=mZ-A14GRfN4&list=PLokeFpXsus96lkVjFsQEMtT5a-yIJKDJt&index=80'
    ]
    for u in range(len(urls)):
        transcript, video_id = yt_video(urls[u])
        data = [t['text'] for t in transcript]
        data = [re.sub(r"[^a-zA-Z0–9-ışğöüçiIŞĞÖÜÇİ ]", "", line) for line in data]
        #print(data)
        text_to_pdf(data, u, video_id)
    print('done!')


#    option = input("\nSearch for word and its timestamp(s)? Y/N\n")
#    if option.lower() == 'y':
#        search_word()


