import os,csv,psycopg2

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# engine = create_engine("postgres://postgres:postgres@localhost:5432/postgres")
# db = scoped_session(sessionmaker(bind=engine))

def connect():
    try:
        conn = psycopg2.connect(
                                host = 'localhost',
                                database = 'postgres',
                                user = 'postgres',
                                password = 'Thao1234',
                                port = '5432')
        cur = conn.cursor()
        print("Successfully connected")

    except Exception as error:
        print('error: ', error)

    return conn,cur

conn, cur = connect()

def main():
    f = open("books.csv", "r")  # needs to be opened during reading csv
    reader = csv.reader(f)
    cur.execute("""
                    set schema 'public';
                    """)
    next(reader)
    for isbn, title, author, year in reader:
        # db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
        #        {"isbn": isbn, "title": title, "author": author, "year": year})
        # db.commit()
        
        insert_script = 'INSERT INTO books (isbn, title, author, year) VALUES (%s, %s, %s, %s)'
        insert_value = (isbn,title,author,year)
        cur.execute(insert_script,insert_value)
        conn.commit()
        print(f"Added book with ISBN: {isbn} Title: {title}  Author: {author}  Year: {year}")


if __name__ == '__main__':
    main()
