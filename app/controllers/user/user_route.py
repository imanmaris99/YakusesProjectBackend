from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from app.utils.db import db
from app.models.user_model import User
import os

user_blueprint = Blueprint('user_endpoint', __name__)
bcrypt = Bcrypt()

@user_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_list_user():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id).first()

        # Cek jika pengguna ditemukan dan jika pengguna adalah admin
        if user is None:
            return jsonify({"message": "User not found"}), 401  # Unauthorized jika pengguna tidak ditemukan

        if user.role != 'admin':
            return jsonify({"message": "You are not authorized to view this resource"}), 401  # Unauthorized jika bukan admin
        
        users = User.query.all()
        user_data = [user.as_dict() for user in users]
        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@user_blueprint.route("/register", methods=["POST"])
def create_user():
    try:
        data = request.json
        # Validasi input
        required_fields = ['username', 'fullname', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing field: {field}"}), 400
        
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
        
        new_user = User(fullname=data["fullname"],
                        username=data["username"],
                        email=data["email"],
                        password=hashed_password,
                        role='member')
        
        db.session.add(new_user)
        db.session.commit()

        # Menyusun data respons
        response_data = new_user.as_dict()

        # Mengembalikan respons dengan status 201
        return jsonify(response_data), 201

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@user_blueprint.route('/login', methods=["POST"])
def login_user():
    data = request.json
    try:
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify({"access_token": access_token}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@user_blueprint.route("/profile", methods=["GET"])
@jwt_required()
def create_user_profile():
    try:
        current_user_id = get_jwt_identity()

        user = User.query.filter_by(id=current_user_id).first()

        if not user:
            return jsonify({"message":"User not found"}), 404
        
        user_data = {
           "my_profile" : user.as_dict(),
           "password" : user.password
        }

        return jsonify(user_data), 200

    except Exception as e:
        return jsonify({"message": str(e)}),500


@user_blueprint.route('/edit', methods=["PUT"])
@jwt_required()  # Membutuhkan token JWT untuk akses
def update_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id).first()

        if user:
            data = request.json
            required_fields = ['phone', 'address', 'about_me']
            for field in required_fields:
                if field in data:  # Perbaiki logika pengecekan
                    setattr(user, field, data[field])

            db.session.commit()
            response_data = user.as_dict()

            return jsonify(response_data), 200
            
        else:
            return jsonify({"message": "User not found"}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@user_blueprint.route("/register/admin", methods=["POST"])
@jwt_required()
def create_user_admin():
    try:
        # Mendapatkan identitas pengguna yang saat ini login dari token JWT
        current_user_id = get_jwt_identity()

        # Querying untuk mendapatkan data pengguna yang saat ini login
        user = User.query.filter_by(id=current_user_id).first()
        
        if user.role != 'admin':
            return jsonify({"message": "Only admins can create other admin users"}), 403
        
        data = request.json
        # Validasi input
        required_fields = ['username', 'firstname', 'lastname', 'email', 'phone', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing field: {field}"}), 400
        
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
        
        new_user_admin = User(username=data["username"],
                        firstname=data["firstname"],
                        lastname=data["lastname"],
                        email=data["email"],
                        facebook=data.get("facebook", None),
                        google=data.get("google", None),
                        phone=data["phone"],
                        password=hashed_password,
                        role='admin')
        
        db.session.add(new_user_admin)
        db.session.commit()

        # Menyusun data respons
        response_data = new_user_admin.as_dict()

        # Mengembalikan respons dengan status 201
        return jsonify(response_data), 201

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@user_blueprint.route('/delete/<int:user_id>', methods=["DELETE"])
@jwt_required()  # Membutuhkan token JWT untuk akses
def delete_profile(user_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=current_user_id).first()

        # Pengecekan apakah pengguna adalah admin
        if current_user.role != 'admin':
            return jsonify({"message": "Unauthorized access"}), 403

        user = User.query.get(user_id)

        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User profile deleted successfully"}), 200
        else:
            return jsonify({"message": "User not found"}), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500