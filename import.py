import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():

    data = pd.read_csv("books.csv", header=0)
    print(data)

    # write all data to records table
    for i in range(0, data.shape[0]):
        db.execute(text("""INSERT INTO records (isbn, title, year, author_name)
                            VALUES(:isbn, :title, :year, :name)"""),
                   {"isbn":data.loc[i, "isbn"], "title":data.loc[i,"title"], "year":int(data.loc[i, "year"]),
                    "name":data.loc[i, "author"]})

    # write authors information into authors table
    authors = db.execute(text("SELECT DISTINCT(author_name) FROM records")).fetchall()
    for author in authors:
        db.execute(text("""INSERT INTO authors (name) VALUES(:name)"""),{"name":author[0]})

    # write books information into books table
    for i in range(0, data.shape[0]):
        # relationship between author name and id
        author_id = db.execute(text("SELECT id FROM authors WHERE name=:name"), {"name":data.loc[i, "author"]}).fetchone()

        db.execute(text("""INSERT INTO books (isbn, title, year, author_id)
                            VALUES(:isbn, :title, :year, :author_id)"""),
                   {"isbn":data.loc[i, "isbn"], "title":data.loc[i,"title"], "year":int(data.loc[i, "year"]),
                    "author_id":author_id[0]})

    # write a user into users table
    db.execute(text("""INSERT INTO users (user_id, password)
                        VALUES(:id, :password)"""),
               {"id": "Roy", "password":"1111"})

    db.commit()


if __name__ == "__main__":
    main()