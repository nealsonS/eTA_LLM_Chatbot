#imported functions
#imported functions
from chatbotParts.dbMilvus import embed
from chatbotParts.ragChain import ai_answer
from chatbotParts.simSearch import sim_search 
# basic libraries to import, some were probably already in imported functions but they are needed here too
#import re
import sys
import json
import time


if __name__ == '__main__':

	arguments = sys.argv
	start = time.time()
	question = " ".join(arguments[1:])  # this version DOES NOT requires users to input questions with ""
	#question = sys.argv[1]  # this version requires users to input questions with ""
	#print(question)

	embeddings, connection_args, COLLECTION_NAME = embed()

	output = ai_answer(question, embeddings, connection_args, COLLECTION_NAME) 
	
	docs, doc_pages, vids, vid_times = sim_search(question, embeddings, connection_args, COLLECTION_NAME)
	# take the 1st items in these lists (top resource?)
	# if there are none, append 1 
	if len(docs) == 0:
		docs.append("none")
	if len(doc_pages) == 0:
		doc_pages.append("none")
	if len(vids) == 0:
		vids.append("none")
	if len(vid_times) == 0:
		vid_times.append("none")
	
	reply = {question: {'output': output,'docs': docs[0], 'pageno': doc_pages[0], 'vids': vids[0], 'vid_time': vid_times[0], 'time': 5.0}}


	q_dict = reply[question.lower()]
	time.sleep(q_dict['time'])

	out_json = {'response': q_dict['output'], 'docs': q_dict['docs'], 'vid_time': q_dict['vid_time'], 'pageno': q_dict['pageno'], 'vids': q_dict['vids']}
	# Good luck & don't stay up all night! :D

	print(json.dumps(out_json))
	end = time.time()
	#print(f'Time elapsed: {end-start}')
