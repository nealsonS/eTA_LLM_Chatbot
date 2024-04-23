from pymilvus import connections
from pymilvus import utility
import os

if __name__ == '__main__':

	host = 'localhost'
	port = '19530'
	URI = f'http://{host}:{port}' # connection address for milvus

	connections.connect(
		alias = 'default',
		host = host,
		port= port
		)

	all_collections = utility.list_collections()

	print('Collections:')
	for i, col in enumerate(all_collections):
		print(f'{i}: {col}')

	print('\nAre you sure you want to delete?')

	input_str = """Please enter:
	- `exit` ALL IN LOWER CASE to exit without `
	- `YES_DELETE_ALL` all in UPPER CASE to delete all without `\nInput: """

	user_input = input(input_str)

	# TO MAKE SURE THINGS NOT DROPPED BY ACCIDENT
	while user_input not in ['exit', 'YES_DELETE_ALL']:

		print("\nInvalid Input!")
		user_input = input(input_str)

	if user_input == 'YES_DELETE_ALL':

		for col in all_collections:
			utility.drop_collection(col)
			print(f'{col} dropped!')


		FILE_DONE_PATH = 'files_inserted.txt'
		if os.path.exists(FILE_DONE_PATH):
			os.remove(FILE_DONE_PATH)
		


