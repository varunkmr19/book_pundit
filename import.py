import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    index = 1
    # create table
    query = "CREATE TABLE books (isbn VARCHAR PRIMARY KEY, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year VARCHAR NOT NULL)"
    db.execute(query)
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        if year == "year":
            print('skipped line 1')
        else:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
            {"isbn": isbn, "title": title, "author": author, "year": year})
        print("Inserted book: " ,index)
        index += 1
    db.commit()

if __name__ == "__main__":
    main()