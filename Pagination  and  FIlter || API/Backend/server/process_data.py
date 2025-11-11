import json
import mysql.connector
import os
from dotenv import load_dotenv

# =============================== ---- Load screats --- =============================================

load_dotenv()
TABLE_NAME = os.getenv("TABLE_NAME")
SQL_ROOT = os.getenv("SQL_ROOT_NAME")
SQL_PASSWORD =os.getenv("SQL_PASSWORD")
SQL_DB_NAME = os.getenv("DATABASE_NAME")
print(SQL_ROOT,SQL_DB_NAME,SQL_PASSWORD)






try:
    mydb = mysql.connector.connect(
        host="localhost", 
        user=SQL_ROOT,
        password=SQL_PASSWORD,
        database=SQL_DB_NAME 
    )

    cursor =  mydb.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INT,
                    cuisine VARCHAR(100),
                    title VARCHAR(200),
                    rating FLOAT,
                    prep_time INT,
                    cook_time INT,
                    total_time INT,
                    description TEXT, 
                    nutrients TEXT,  
                    serves VARCHAR(100) 
            );""")
     


    
  
    # ======================================= ------ process the datas ------ ==========================================================

    insert_query = """
          INSERT INTO RecipeData 
         (id, cuisine, title, rating, prep_time, cook_time, total_time, description, nutrients, serves) 
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
         """



    with open("/home/nandhiraja/Nandhiraja C/Securin_Project/Backend/Data/US_recipes_null.json", 'r') as file:
        data = json.load(file)




    print("start_process...")
    limit = 0
    rows_to_insert = []

    for index in data:
        
        value = data[index]
        nutrients_json_string = json.dumps(value["nutrients"])

        row_data = (
            int(index), 
            value["cuisine"], 
            value["title"], 
            value["rating"], 
            value["prep_time"], 
            value["cook_time"], 
            value["total_time"], 
            value["description"], 
            nutrients_json_string,
            value["serves"]
        )
        rows_to_insert.append(row_data)
        limit += 1

    print("done processing data into list.")

    cursor.executemany(insert_query, rows_to_insert)
    mydb.commit()
    cursor.close()
    print("done addend in db")

except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")


if __name__ == "__main__":
    # process_data(data)
    pass