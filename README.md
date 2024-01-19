# Library Management System - Flask REST API

This is a simple Flask-based REST API for a Library Management System.

1. Clone the repository:

   ```bash
   https://github.com/joy1954islam/Flask-Library-Management-System.git
   cd Flask-Library-Management-System
   
2. Create a virtual environment (optional but recommended):
    ```bash
        virtualenv venv
        source venv/bin/activate
        On Windows, use venv\Scripts\activate

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
   
4. Run the Application
Run the Flask application:

    ```bash
    python app.py


# API Endpoints
 - POST /books: Add a new book to the database.
- GET /books: Retrieve a list of all books in the database.
- GET /books/<id>: Retrieve details of a specific book by ID.
- PUT /books/<id>: Update the details of a specific book.
- DELETE /books/<id>: Delete a book from the database.