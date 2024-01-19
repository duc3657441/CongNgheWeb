## Overview

This web site features 5000 hand picked books allowing users to search, leave reviews for individual books, and see the reviews made by other people. It also uses a third-party API by Goodreads.com, another book review website, to pull ratings from a broader audience. In addition, users are able to query for book details and book reviews programmatically via website's API. 

# Installation

## Pre-requisites

Make sure you have the following installed on your machine:
* postgreSQL
* Python 3.7.2

## Proceed to download
1. Clone the repository
2. In your terminal window, navigate into the project
3. Run `pip3 install -r requirements.txt` to make sure all of the necessary Python packages (Flask, SQLAlchemy and others) are installed
4. Set the environment variables:
	  * `export FLASK_APP=application.py`. On Windows, the command is instead` set FLASK_APP=application.py`
    - `KEY` = is your API key, will give you the review and rating data for the book with the provided ISBN number (register at goodreads.com)
    - `DATABASE_URL` = URI for your local postgreSQL database (for example: `postgres://username:password@localhost:5432/databasename` )
5. Run `tables.sql` against your database to create the necessary tables
  ![Alt text](db-schema.png?raw=true "Title")
6. Run `python3 import.py` to import a spreadsheet in CSV format of 5000 different books to your database
7. Finally execute `flask run` command in your terminal to start the server
