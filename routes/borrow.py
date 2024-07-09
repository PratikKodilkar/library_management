from flask import Blueprint, request, jsonify, make_response
from models import db, User, Book, Borrow
from datetime import datetime

borrow_bp = Blueprint('borrow_bp', __name__)

# borrow a book
@borrow_bp.route('/borrow', methods=['POST'])
def borrow_book():
    try:
        data = request.get_json()

        # validate if 'user_id' and 'book_id' are present
        if 'user_id' not in data or 'book_id' not in data:
            return make_response(jsonify({'message': 'user_id and book_id are required'}), 400)
        
        # validate if 'user_id' and 'book_id' are integers
        try:
            user_id = int(data['user_id'])
            book_id = int(data['book_id'])
        except Exception as e:
            return make_response(jsonify({'message': 'user_id and book_id must be integers', 'error': str(e)}), 400)
        
        # check if user exists
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return make_response(jsonify({'message': 'user not found'}), 404)
        
        # check if book exists
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            return make_response(jsonify({'message': 'book not found'}), 404)

        if book.available:
            today_str = datetime.today().strftime('%Y-%m-%d')
            today = datetime.strptime(today_str, '%Y-%m-%d').date()
            borrow = Borrow(user_id=data['user_id'], book_id=data['book_id'], borrow_date=today)
            db.session.add(borrow)
            db.session.commit()
            book.available = False
            db.session.add(book)
            db.session.commit()
            return make_response(jsonify({'message': 'Book borrowed successfully', 'borrow_date': today}), 200)
        else:
            return make_response(jsonify({'message': 'Book is not available'}), 400)
    except Exception as e:
        return make_response(jsonify({'message': 'error in borrowing of book', 'error': str(e)}), 500)


# return a book
@borrow_bp.route('/return', methods=['POST'])
def return_book():
    try:
        data = request.get_json()

        # Validate if 'user_id' and 'book_id' are present
        if 'user_id' not in data or 'book_id' not in data:
            return make_response(jsonify({'message': 'user_id and book_id are required'}), 400)
        
        # Validate if 'user_id' and 'book_id' are integers
        try:
            user_id = int(data['user_id'])
            book_id = int(data['book_id'])
        except Exception as e:
            return make_response(jsonify({'message': 'user_id and book_id must be integers', 'error': str(e)}), 400)
        
        # Check if 'user_id' exists
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return make_response(jsonify({'message': 'user not found'}), 404)

        # Check if 'user_id' exists
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            return make_response(jsonify({'message': 'book not found'}), 404)
        
        # Find the borrow entry
        borrow = Borrow.query.filter_by(user_id=data['user_id'], book_id=data['book_id'], return_date=None).first()
        if not borrow:
            return make_response(jsonify({'message': 'No active record found for this user and book'}), 404)

        if not book.available:
            today_str = datetime.today().strftime('%Y-%m-%d')
            today = datetime.strptime(today_str, '%Y-%m-%d').date()
            borrow.return_date=today
            db.session.add(borrow)
            db.session.commit()
            book.available = True
            db.session.add(book)
            db.session.commit()
            return make_response(jsonify({'message': 'Book returned successfully', 'return_date': today}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error in returning book', 'error': str(e)}), 500)


# get all books borrowed by an individual user
@borrow_bp.route('/users/<int:user_id>/borrowed', methods=['GET'])
def get_borrow(user_id):
    try:
        # Check if 'user_id' exists
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return make_response(jsonify({'message': 'user not found'}), 404)
        
        # Validate if 'user_id' is integer
        try:
            user_id = int(user_id)
        except Exception as e:
            return make_response(jsonify({'message': 'user_id must be integer', 'error': str(e)}), 400)

        borrows = Borrow.query.filter_by(user_id=user_id, return_date=None).all()
        if borrows:
            return make_response(jsonify({'user_id': user_id, 'borrowed_books': [borrow.json() for borrow in borrows]}), 200)
        else:
            return make_response(jsonify({'message': 'No active borrow records found for this user'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error fetching borrow records', 'error': str(e)}), 500)