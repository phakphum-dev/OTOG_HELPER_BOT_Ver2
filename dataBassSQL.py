import psycopg2 as sql

thatCursor = None
con = None



def exeAndGet(*arg):
    for e in arg:
        thatCursor.execute(e)
    return thatCursor.fetchall()

def isTableExist(nameTable:str) -> bool:
    return exeAndGet(f"SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename  = '{nameTable}');")[0][0]

def exeAndCommit(*arg):
    for e in arg:
        thatCursor.execute(e)
    con.commit()

def initData(dbName: str, dbUser: str, dbPassword: str, dbHost: str, dbPort : str):
    global thatCursor, con
    con = sql.connect(database=dbName,
                      user=dbUser,
                      password=dbPassword,
                      host=dbHost,
                      port=dbPort)
    thatCursor = con.cursor()

    if not isTableExist("gng"):
        print("SQL : gng table not found...",end='')
        exeAndCommit("CREATE TABLE gng ( \
            iduser BIGINT, \
            remain INT DEFAULT 7, \
            iscorrect BOOLEAN DEFAULT FALSE, \
            istroll BOOLEAN, \
            correct BIGINT \
        ); \
        ")
        print("completed")

    if not isTableExist("verify"):
        print("SQL : verify table not found...",end='')
        exeAndCommit("CREATE TABLE verify ( \
            iduser BIGINT, \
            num SMALLINT, \
            code TEXT \
        ); \
        ")
        print("completed")
    
    if not isTableExist("music"):
        print("SQL : music table not found...",end='')
        exeAndCommit("CREATE TABLE music ( \
            serverid BIGINT, \
            vcid BIGINT, \
            link TEXT, \
            title TEXT, \
            path TEXT, \
            len REAL,\
            sid BIGINT\
        ); \
        ")
        print("completed")


if __name__ == "__main__":
    envConfig = dict()
    with open(".env","r") as f:
        for line in f:
            if line.strip()[0] != "#" and '=' in line:
                envConfig[line.split('=')[0]] = ("=".join(line.split('=')[1:])).strip()

    initData(envConfig["DB_DATABASE"], envConfig["DB_USERNAME"], 
                 envConfig["DB_PASSWORD"], envConfig["DB_HOST"],
                 envConfig["DB_PORT"])
    
    res = checkTableExist("gng")
    print(res, type(res))