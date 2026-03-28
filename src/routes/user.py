from flask import Blueprint, jsonify, request
from src.models.user import User, db
from sqlalchemy import text
import uuid

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({'error': 'username required'}), 400
    try:
        # Some DB schemas still require an email NOT NULL column. Insert with empty string
        # create a unique dummy email to satisfy existing DB NOT NULL + UNIQUE constraints
        dummy_email = f"{username}_{uuid.uuid4().hex}@local"
        res = db.session.execute(
            text('INSERT INTO "user" (username, email) VALUES (:username, :email) RETURNING id'),
            {'username': username, 'email': dummy_email}
        )
        user_id = res.scalar()
        db.session.commit()
        user = User.query.get(user_id)
        return jsonify(user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.username = data.get('username', user.username)
    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # delete user's notes first to avoid foreign key issues
    from src.models.note import Note
    Note.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    return '', 204
