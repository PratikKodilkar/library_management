from flask import Blueprint, request, jsonify, make_response
from config import db
from models import User

users_bp = Blueprint('users_bp', __name__)

# create a user
@users_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'user created'}), 201)
    except Exception as e:
        users_bp.logger.error(f"Error creating user: {e}")
        return make_response(jsonify({'message': 'error creating user', 'error': str(e)}), 500)

# get all users
@users_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    except Exception as e:
        users_bp.logger.error(f"Error getting users: {e}")
        return make_response(jsonify({'message': 'error getting users', 'error': str(e)}), 500)

# get user by id
@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'user': user.json()}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        users_bp.logger.error(f"Error getting user: {e}")
        return make_response(jsonify({'message': 'error getting user', 'error': str(e)}), 500)

# update user by id
@users_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.name = data['name']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message': 'user updated'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        users_bp.logger.error(f"Error updating user: {e}")
        return make_response(jsonify({'message': 'error updating user', 'error': str(e)}), 500)
    
# delete user by id
@users_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        users_bp.logger.error(f"Error deleting user: {e}")
        return make_response(jsonify({'message': 'error deleting user', 'error': str(e)}), 500)
