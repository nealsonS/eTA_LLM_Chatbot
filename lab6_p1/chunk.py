import mysql.connector
from langchain.text_splitter import CharacterTextSplitter


def connect_to_database(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            table_name = 'cookbook'
            query = f"SELECT text_content FROM {table_name}"
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            #for row in rows:
            #    print(row)
            return rows
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def get_text_chunks(text_content):
    for t in text_content:
        text = str(t)
        text_splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=500, #must be 500
            chunk_overlap=100,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        for c in range(len(chunks)):
            print(c, "-----------------")
            print(chunks[c])
    #return chunks
    
 
 
def main():
    host = 'localhost' # get this from main code
    user = 'root'
    password = ''
    database = 'demo1'
    raw_text = connect_to_database(host, user, password, database)

    text_chunks = get_text_chunks(raw_text)
 



if __name__ == '__main__':
    main()
