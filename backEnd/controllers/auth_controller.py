import bcrypt
from bson import ObjectId
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from models.Teacher import Teacher
from models.Student import Student
from middleware.global_middleware import verify_user

from db.bd_mysql import db_connection

def login_controller(data):
    try:
        email = data.get('email', '').lower()
        password = data.get('password', '')

        if not email or not password:
            return {"message": "Email or password is missing"}, 400

        connection = db_connection()
        if not connection:
            return {"message": "Database connection error"}, 500
        
        user = Student.get_student_by_email_service(connection, email)
        user_type = 'student'

        if not user:
            user = Teacher.get_teacher_by_email_service(connection, email)
            user_type = 'teacher'

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.get('password', '').encode('utf-8')):
                access_token = create_access_token(identity={'id': str(user['id']), 'type': user_type})
                return {"access_token": access_token}, 200
            else:
                return {"message": "Invalid email or password"}, 401
        else:
            return {"message": "Invalid email or password"}, 401

    except Exception as e:
        return {"message": str(e)}, 500

    finally:
        if connection:
            connection.close()




def get_user_data():
    user_id = get_jwt_identity()
    user_data = Student.get_user_by_id_model(ObjectId(user_id))
    if user_data:
        user_data.pop('password', None)
        user_data['_id'] = str(user_data['_id'])
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'User not found'}), 404