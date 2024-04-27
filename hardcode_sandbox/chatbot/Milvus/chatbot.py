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
	#print(hard_coded_questions)

	# HARDCODE FOR DEMO PURPOSES!
	#hard_coded_questions = {'what are macromolecules?': {'output': "Macromolecules are large molecules with a molecular mass in kilodaltons (kDa), such as proteins, glycoproteins, or monoclonal antibodies, either as intact immunoglobulins or as their fragments. These molecules are significant in biotechnology and medicine, often used in targeted therapies and as diagnostic aids. The term encompasses both naturally occurring and synthetic molecules used in various applications, including drug development and disease treatment."
	#,'docs': '', 'pageno': 0, 'vids': 'HzeICXXGB-Q', 'vid_time': 734, 'time': 7.585682153701782},
	#'what are quality assessments of drug therapy?': {'output': 'Quality assessments of drug therapy involve evaluating and improving the use of medications within healthcare settings to optimize patient outcomes and minimize risks such as medication errors and adverse drug events. These assessments focus on the entire medication-use process, from selection and administration to monitoring and ongoing evaluation, using tools like benchmarking, guidelines, and quality improvement programs. The goal is to ensure safe, effective, and economical medication use.', 
	#'docs': '../all_course_materials/principles_clinical_pharmacology.pdf', 'pageno': 503, 'vids': '', 'vid_time': 0, 'time': 5.448596477508545}}

	q_dict = reply[question.lower()]
	time.sleep(q_dict['time'])

	out_json = {'response': q_dict['output'], 'docs': q_dict['docs'], 'vid_time': q_dict['vid_time'], 'pageno': q_dict['pageno'], 'vids': q_dict['vids']}
	# Good luck & don't stay up all night! :D

	print(json.dumps(out_json))
	end = time.time()
	#print(f'Time elapsed: {end-start}')
