import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
from typing import Dict
import json
load_dotenv()
TABLE_NAME = os.getenv("TABLE_NAME")
SQL_ROOT = os.getenv("SQL_ROOT_NAME")
SQL_PASSWORD =os.getenv("SQL_PASSWORD")
SQL_DB_NAME = os.getenv("DATABASE_NAME")
print(SQL_ROOT,SQL_DB_NAME,SQL_PASSWORD)


my_database = None
cursor =None
try:
    my_database = mysql.connector.connect(
        host="localhost", 
        user=SQL_ROOT,
        password=SQL_PASSWORD,
        database=SQL_DB_NAME 
    )
    cursor =  my_database.cursor()

except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")

# def get_total_recipes():
#     return cursor.execute(F"select count(*) from {TABLE_NAME}")

def get_recipes(page:int,limit:int):
    if(limit<0):
        limit=1
    if(page<0):
        page=0
    query_string = f"SELECT * FROM {TABLE_NAME} LIMIT {limit} OFFSET {page*limit} "
    cursor.execute(query_string)
    sql_data = cursor.fetchall()

    result = {}
    index=0;
    for data in sql_data:
        result[f'{index}']={
            "id":data[0],
            "cuisine":data[1],
            "title":data[2],
            "rating":data[3],
            "prep_time":data[4],
            "cook_time":data[5],
            "total_time":data[6],
            "description":data[7],
            "nutrients":json.loads(data[8]),
            "serves":data[9]
        }
        index+=1






    return  result



def search_data(params:Dict):

    search_query_string = f"SELECT * FROM {TABLE_NAME} WHERE "
    for operation  in params.keys():
     
        if operation in ["total_time",'rating']:
            search_query_string += f" {operation} {params[operation][0]}={params[operation][1]} and" 
            continue
        search_query_string += f" {operation}  LIKE '% {params[operation]} %' and" 
    
    cursor.execute(search_query_string.rstrip("and"))
    print(search_query_string ,"\n",search_query_string.rstrip("and"))

    sql_data = cursor.fetchall()

    result = {}
    index=0;
    for data in sql_data:
        result[f'{index}']={
            "id":data[0],
            "cuisine":data[1],
            "title":data[2],
            "rating":data[3],
            "prep_time":data[4],
            "cook_time":data[5],
            "total_time":data[6],
            "description":data[7],
            "nutrients":json.loads(data[8]),
            "serves":data[9]
        }
        index+=1






    return  result
    # return {"hai"}
