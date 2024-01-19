from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from datetime import datetime
from flask_restful import Api, Resource, reqparse, abort
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:171-35-1954@localhost:5432/flask_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'  # Use your preferred database URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)


app.app_context().push()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(13), nullable=False, unique=True)
    published_year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"{self.title}:{self.author}"


class BaseSchema(Schema):
    def handle_validation_error(self, error):
        return {'message': 'Validation error', 'errors': error.messages}, 400


class BookSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    isbn = fields.Str(required=True)
    published_year = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


book_schema = BookSchema()
books_schema = BookSchema(many=True)


class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return book_schema.dump(book)

    def put(self, book_id):
        book = Book.query.get_or_404(book_id)
        data = request.get_json()

        try:
            updated_book_data = book_schema.load(data, partial=True)
        except ValidationError as e:
            return {'message': 'Validation error', 'errors': e.messages}, 400

        # Update fields manually
        for key, value in updated_book_data.items():
            setattr(book, key, value)

        db.session.commit()
        return book_schema.dump(book)

    def delete(self, book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {"message": 'Delete Successfully'}, 200


class BooksResource(Resource):
    def get(self):
        books = Book.query.all()
        return books_schema.dump(books)

    def post(self):
        data = request.get_json()

        try:
            new_book_data = book_schema.load(data)
            new_book = Book(**new_book_data)
        except ValidationError as e:
            return {'message': 'Validation error', 'errors': e.messages}, 400

        db.session.add(new_book)
        db.session.commit()
        return book_schema.dump(new_book), 201


# Step 1: Set up Flask application and configure the database
if __name__ == '__main__':
    db.create_all()
    api.add_resource(BooksResource, '/books')
    api.add_resource(BookResource, '/books/<int:book_id>')
    app.run(debug=True)
