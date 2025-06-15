import psycopg2

# database connection variables
# TODO: need a way to not have to comment this
# ec2 credentials 
HOST = '172.17.0.1'
USER = 'postgres'
# local credentials
# HOST = 'host.docker.internal' # this is for running inside the container
# USER = 'tristanallen'
DATABASE = "trading_post"
DB_PORT = "5432"
# table names
TICKER_NEWS_TABLE = "ticker_news"
NEWS_ARTICLES_TABLE = "news_articles"
RELATED_TICKER_TABLE = "related_tickers"
# columns 
ARTICLE_ID_COL = "article_id"
ARTICLE_TITLE_COL = "article_title"
ARTICLE_AUTHOR_COL = "article_author"
ARTICLE_URL_COL = "article_url"
ARTICLE_DESC_COL = "article_desc"
# test variables
TEST_TABLE = "ticker_news"
TEST_TICKER = "MSFT"
TEST_RELATED = [ "AMZN", "NVDA", "DIS" ]
TEST_DATE = "2025-06-06"
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
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"failed insert '{curTuple}' into '{table}'")
        print(f"ERROR: {e}")
        return 2
    # cleanup
    curCursor.close()
    return 0

def sqlSelect(table: str, select: list[str]=None, join: list[str]=None, where: dict=None) -> list[tuple]:
    """
    sqlSelect: executes a SQL select statement on a given table \\
    parameters: \\
        table - str, name of table to select values from \\
        select - list, column names to select from \\
        join - list, list of join statements \\
        where - dict, \\
    returns: a list of tuples replresenting the query results
    """
    curCursor = connection.cursor()
    # setup SELECT str
    columnStr = ""
    if select:
        for col in select:
            columnStr += f"{col}, "
        columnStr = columnStr[:-2]
    else:
        columnStr = "*"
    # setup JOIN string
    joinStr = ""
    # TODO: Not sure is having 'join' as a list is best but it should be fine for now
    if join:
        joinStr = f" JOIN {join[0]} ON {join[1]}={join[2]}"
    # setup WHERE string
    whereStr = ""
    if where:
        whereStr = " WHERE "
        for key in list(where.keys()):
            whereStr += f"{key}='{where[key]}'"
    # running the sql statement
    sqlStr = f"SELECT {columnStr} FROM {table}{joinStr}{whereStr};"
    print(f"sql statement: {sqlStr}")
    try:
        curCursor.execute(sqlStr)
        connection.commit()
        # fetching the results
        queryResults = curCursor.fetchall()
    except Exception as e:
        connection.rollback()
        print(f"failed table: {table}")
        print(f"ERROR: {e}")
        queryResults = []
    # cleanup
    curCursor.close()
    return queryResults

def sqlDelete(table: str, where: dict=None) -> int:
    """
    sqlDelete: executes a SQL delete statement on a given table \\
    parameters: \\
        table - str, name of table to select values from \\
        where - dict, \\
    returns: \\
        0 - success \\
        1 - failed to execute sql command
    """
    curCursor = connection.cursor()
    # setup WHERE string
    whereStr = ""
    if where:
        whereStr = " WHERE "
        for key in list(where.keys()):
            whereStr += f"{key}='{where[key]}'"
    # running the sql statement
    sqlStr = f"DELETE FROM {table}{whereStr};"
    try:
        curCursor.execute(sqlStr)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"failed table: {table}")
        print(f"ERROR: {e}")
        return 1
    # cleanup
    curCursor.close()
    return 0

if __name__ == "__main__":
    # sqlInsert(TEST_TABLE, TEST_INSERT)
    # sqlInsert(TEST_TABLE, TEST_INSERT)
    # print(sqlSelect(TEST_TABLE, where={"ticker_symbol": "APPL"}))
    print(sqlDelete(TICKER_NEWS_TABLE, { "ticker_symbol": "GOOGL" }))