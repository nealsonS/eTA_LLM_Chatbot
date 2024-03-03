import json
import mysql.connector
from mysql.connector import errorcode
import execjs


def get_user_password():
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'
    password = input("Please enter your MySQL password:\n")
    return user, password


def connect_to_database(host, user, password, database):
    try:
        return mysql.connector.connect(host=host, user=user, password=password, database=database)
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        sys.exit(1)


def run_map_js(latitude, longitude):
    with open("main.js", "r") as file:
        js_code = file.read()
    context = execjs.compile(js_code)
    result = context.call("coordinates", latitude, longitude)
    print(result)



if __name__ == "__main__":
    host = 'localhost'
    user, password = get_user_password()
    database = input("Please enter your MySQL database:\n")
    
    connection = connect_to_database(host, user, password, database)
    print("Connected to the database.")
    cursor = connection.cursor()
    
    print("Gathering information from database.")
    latitude = []
    longitude = []
    well_name = []
    address = []
    well_status = []
    well_type = []
    closest_city = []
    barrels_of_oil = []
    barrels_of_gas = []
    try:
        with connection.cursor(dictionary=True) as cursor:
            # get data from database
            sql = "SELECT longitude, latitude, well_name, address, well_status, well_type, closest_city, barrels_of_oil, barrels_of_gas FROM well_data"
            cursor.execute(sql)
            # store location data
            for row in cursor.fetchall():
                latitude.append(row['latitude'])
                longitude.append(row['longitude'])
                well_name.append(row['well_name'])
                address.append(row['address'])
                well_status.append(row['well_status'])
                well_type.append(row['well_type'])
                closest_city.append(row['closest_city'])
                barrels_of_oil.append(row['barrels_of_oil'])
                barrels_of_gas.append(row['barrels_of_gas'])              
                
    finally:
        cursor.close()
        connection.close()
    #print(json.dumps(longitude))
    run_map_js(latitude, longitude)
    print("Run this command to see the map: npm start")
