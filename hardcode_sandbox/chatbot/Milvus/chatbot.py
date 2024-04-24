import re
import sys
import json
import time


if __name__ == '__main__':

	start = time.time()
	question = sys.argv[1]

	# HARDCODE FOR DEMO PURPOSES!
	hard_coded_questions = {'what are macromolecules?': {'output': "Macromolecules are large molecules with a molecular mass in kilodaltons (kDa), such as proteins, glycoproteins, or monoclonal antibodies, either as intact immunoglobulins or as their fragments. These molecules are significant in biotechnology and medicine, often used in targeted therapies and as diagnostic aids. The term encompasses both naturally occurring and synthetic molecules used in various applications, including drug development and disease treatment."
	,'docs': '', 'vids': 'V5hhrDFo8Vk', 'time': 7.585682153701782},
	'what are quality assessments of drug therapy?': {'output': 'Quality assessments of drug therapy involve evaluating and improving the use of medications within healthcare settings to optimize patient outcomes and minimize risks such as medication errors and adverse drug events. These assessments focus on the entire medication-use process, from selection and administration to monitoring and ongoing evaluation, using tools like benchmarking, guidelines, and quality improvement programs. The goal is to ensure safe, effective, and economical medication use.', 
	'docs': '../all_course_materials/principles_clinical_pharmacology.pdf', 'vids': '', 'time': 5.448596477508545}}

	q_dict = hard_coded_questions[question.lower()]
	time.sleep(q_dict['time'])

	out_json = {'response': q_dict['output'], 'docs': q_dict['docs'], 'vids': q_dict['vids']}

	print(json.dumps(out_json))
	end = time.time()
	#print(f'Time elapsed: {end-start}')


