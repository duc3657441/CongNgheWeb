import psycopg2
#Connect to database
def connect():
    try:
        conn = psycopg2.connect(
                                host = 'localhost',
                                database = 'CongNgheWebTest',
                                user = 'postgres',
                                password = '159357',
                                port = '5432')
        cur = conn.cursor()
        
        cur.execute("SET schema 'DatabaseWeb';")
        print("Successfully connected")
    except Exception as error:
        print('error: ', error)

    return conn,cur
