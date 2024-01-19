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

# conn, cur = connect()
# form_email = str('nguyendinhduc@gmail.com')
# try: 
    
#     query = "SELECT * FROM users WHERE email LIKE %s"
#     value = (form_email,)
#     cur.execute(query,  value)
      
# except Exception as e: 
#     print('error: ', e)

# data = cur.fetchone()

# print('UserID: ', data[0]) 
# print('firstName: ', data[1]) 
# # print('lastName: ', data.lastName) 
# # print('email: ', data.email)
# # print('password',data.password) 
# print('----------------------------------') 