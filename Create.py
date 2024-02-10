import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():

    # create tables
    db.execute(text("""CREATE TABLE Authors (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR NOT NULL);"""))
    db.execute(text("""CREATE TABLE Books (
                        isbn VARCHAR PRIMARY KEY,
                        title VARCHAR NOT NULL,
                        year INT NOT NULL,
                        author_id INT NOT NULL);"""))
    db.execute(text("""CREATE TABLE Records (
                        isbn VARCHAR PRIMARY KEY,
                        title VARCHAR NOT NULL,
                        year INT NOT NULL,
                        author_name VARCHAR);"""))
    db.execute(text("""CREATE TABLE users (
                        user_id VARCHAR PRIMARY KEY,
                        password VARCHAR NOT NULL);"""))
    db.commit()


if __name__ == "__main__":
    main()