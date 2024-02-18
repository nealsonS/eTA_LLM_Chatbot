#from get_mysql_data import get_dataset_from_mysql 
#from topic_modeling_p1 import topic_modeling 
from keyword_extraction_p1 import store_posts
from optnumtop import optnumtop


# need scraping, preprocessing, and storage that is updated every X minutes

# while not updating, take keyword, then it should be clustered again and output the cluster topic and a graphical representation.



if __name__ == '__main__':
    interval = input("Input the interval in minutes that the database will be updated (EX: '5' for 5 minutes)\n")
    print(interval)
    store_posts('tech', 100)
    #topic_modeling()
    optnumtop()
