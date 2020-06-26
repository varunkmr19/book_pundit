# Project 1

Web Programming with Python and JavaScript

BookPundit is a book review webiste. In which a user can read as well as write his/her own reviews on a collection of 5000 books.
I've used flask and python as a backend and for database I'm using postgres sql.
In this project I've used flask, python and postgres as database.

###### Short description of the various file contained in the project

* _Application.py:_ This file is used to run the main application.
* _init.py_: This file binds the application with the database and all the other neccessary packages.
* _forms.py_: This file contains the all the forms used in the project as an flask form object.
* _models.py_: This file contains all the ORMs like Book, User and Review.
* _route.py_: This file contains all the routes as well as the functions to retrive and post all the necessary queries.

###### How to run
First of all you have to set the environment varibale DATABASE_URL as your heroku postgress database URI.
Open terminal or cmd (Windows) and type in the following command
* on Mac/Linux use `export DATABASE_URL=your database URI`
* on Windows use 'set DATABASE_URL=your database URI`

After that run application.py as a python program

###### API Doc
You can request the details of the book using its isbn. Like GET _"/api/isbn"_
