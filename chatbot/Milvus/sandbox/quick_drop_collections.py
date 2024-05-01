from pymilvus import connections
from pymilvus import utility

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

	for col in all_collections:
		utility.drop_collection(col)
		print(f'{col} dropped!')


