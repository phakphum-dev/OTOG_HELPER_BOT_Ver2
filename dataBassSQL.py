import psycopg2 as sql

thatCursor = None
con = None


def initData(dbName: str, dbUser: str, dbPassword: str, hostt: str):
    global thatCursor, con
    con = sql.connect(database=dbName,
                      user=dbUser,
                      password=dbPassword,
                      host=hostt)
    thatCursor = con.cursor()


def exeAndGet(*arg):
    for e in arg:
        thatCursor.execute(e)
    return thatCursor.fetchall()


def exeAndCommit(*arg):
    for e in arg:
        thatCursor.execute(e)
    con.commit()
