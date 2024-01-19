import csv
from app.connect import connect


def main():
    conn, cur = connect()
    f = open("books.csv", "r")  # needs to be opened during reading csv
    reader = csv.reader(f)
  
    # cur.execute("SET schema 'DatabaseWeb';")
    next(reader)
    for isbn, title, author, year in reader:

        insert_script = 'INSERT INTO books (isbn, title, author, year) VALUES (%s, %s, %s, %s)'
        insert_value = (isbn,title,author,year)
        cur.execute(insert_script,insert_value)
        conn.commit()
        print(f"Added book with ISBN: {isbn} Title: {title}  Author: {author}  Year: {year}")

    conn.close()

if __name__ == '__main__':
    main()
