import os
import mysql.connector

HOST = 'localhost'
USER = 'root'
DATABASE = "OptionsHistorical"

# sqlInsert: executes a SQL insert statement on a given table
# parameters: 
# 	table - str, name of table to insert values into 
#	curTuple - tuple, tuple of values to insert into table 	
def sqlInsert(table, curTuple):
    try: 
        connection = mysql.connector.connect(host=HOST, user=USER, database=DATABASE) 
    except Exception as e:
        print(f'error: {e}')
        return 1
    curCursor = connection.cursor()
    # actually inserting into the table
    curValStr = "%s, " * len(curTuple) # "%s, %s, ..., %s"
    sqlStr = f"INSERT INTO {table} VALUES ({curValStr[:-2]});"
    try:
        curCursor.execute(sqlStr, curTuple)
    except Exception as e:
        print(f"failed table: {table}")
        print(f"failed insert: {curTuple}")
        print(f"ERROR: {e}")
        return 2
    # cleanup
    connection.commit()
    curCursor.close()
    return 0

def resetDatabase(database: str):
    os.system(f'mysql -e "CREATE DATABASE IF NOT EXISTS {database}"')
    os.system(f'mysql {database} < "{os.getcwd()}/options_db_schema.sql"')
