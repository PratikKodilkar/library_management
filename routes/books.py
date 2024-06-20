from flask import Blueprint, request, jsonify, make_response
from models import db, Book
from datetime import datetime

books_bp = Blueprint('books_bp', __name__)

# add a new book
@books_bp.route('/books', methods=['POST'])
def add_book():
    try:
        data = request.get_json()
        new_book = Book(title=data['title'], 
                        author=data['author'], 
                        published_date=datetime.strptime(data['published_date'], '%Y-%m-%d').date())
        db.session.add(new_book)
        db.session.commit()
        return make_response(jsonify({'message': 'new book added'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error adding a new book', 'error': str(e)}), 500)
    
# get a book by id
@books_bp.route('/books/<int:id>', methods=['GET'])
def get_books(id):
    try:
        book = Book.query.filter_by(id=id).first()
        if book:
            return make_response(jsonify({'book': book.json()}), 200)
        return make_response(jsonify({'message': 'book not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting book details', 'error': str(e)}), 500)
    
# update a book by id
@books_bp.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    try:
        book = Book.query.filter_by(id=id).first()
        if book:
            data = request.get_json()
            book.title = data['title']
            book.author = data['author']
            book.published_date = datetime.strptime(data['published_date'], '%Y-%m-%d').date()
            db.session.commit()
            return make_response(jsonify({'message': 'book details got updated'}), 200)
        return make_response(jsonify({'message': 'book not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating book', 'error': str(e)}), 500)
    
# delete a book by id
@books_bp.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    try:
        book = Book.query.filter_by(id=id).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return make_response(jsonify({'message': 'book deleted'}), 200)
        return make_response(jsonify({'message': 'book not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting a book', 'error': str(e)}), 500)

