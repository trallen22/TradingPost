from curses import curs_set
import os
import psycopg2

# database connection variables
HOST = 'host.docker.internal' # this is for running inside the container
USER = 'tristanallen'
DATABASE = "trading_post"
DB_PORT = "5432"
# test variables
TEST_TABLE = "related_tickers"
TEST_TICKER = "APPL"
TEST_RELATED = [ "GOOG", "META" ]
TEST_DATE = "2025-06-07"
TEST_INSERT = (TEST_TICKER, f'{TEST_RELATED}', TEST_DATE)
TEST_SELECT_COLS = [ "ticker_symbol", "related_tickers" ]

# we'll try to open a connection 
try: 
    connection = psycopg2.connect(host=HOST, user=USER, database=DATABASE, port=DB_PORT) 
except Exception as e:
    print(f"ERROR: failed to connect to database")
    print(f'error: {e}')
    exit(1)

def sqlInsert(table: str, curTuple: tuple[str,str,str]) -> int:
    """
    sqlInsert: executes a SQL insert statement on a given table \\
    parameters: \\
    	table - str, name of table to insert values into \\
    	curTuple - tuple, tuple of values to insert into table \\
    returns: \\
        0 - success \\
        1 - connection failed \\
        2 - execution failed
    """
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

def sqlSelect(table: str, columns: list[str]):
    curCursor = connection.cursor()
    columnStr = ""
    for col in columns:
        columnStr += f"{col}, "
    # running the sql statement
    sqlStr = f"SELECT {columnStr[:-2]} FROM {table};"
    try:
        curCursor.execute(sqlStr)
    except Exception as e:
        print(f"failed table: {table}")
        print(f"failed col string: {columnStr}")
        print(f"ERROR: {e}")
        return []
    # fetching the results
    queryResults = curCursor.fetchall()
    # cleanup
    connection.commit()
    curCursor.close()
    return queryResults

if __name__ == "__main__":
    # sqlInsert(TEST_TABLE, TEST_INSERT)
    print("test")
    print(sqlSelect(TEST_TABLE, "*"))