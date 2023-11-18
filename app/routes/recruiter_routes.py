from flask import Blueprint, request
from app.models import Recruiter, db
import jwt
import os
from passlib.hash import pbkdf2_sha256
from app import success, fail, successWithData
from dotenv import load_dotenv
recruiter_bp = Blueprint('recruiter', __name__)
load_dotenv()



# register
@recruiter_bp.route("/register", methods=['POST'])
def register_recruiter():
    try:
        data = request.get_json()
        hashed = pbkdf2_sha256.using(rounds=10, salt_size=16).hash(data['password'])
        new_user = Recruiter(
            name=data['name'],
            email=data['email'],
            password=hashed,
            token="",
            company_name=data['company_name'],
            company_address=data['company_address'],
            city=data['city'],
            state=data['state'],
            pincode=data['pincode']
        )

        db.session.add(new_user)
        db.session.commit()
        return success("Register successfully!")
    except Exception as e:
        return fail(str(e)), 401
    

# login 
@recruiter_bp.route('/login', methods=['POST'])
def login_recruiter():
    try:
        data = request.get_json()

        if 'email' in data:
            user = Recruiter.query.filter_by(email=data['email']).first()
            if(user and pbkdf2_sha256.verify(data['password'], user.password)):
                if(user.token == ""):
                    token = jwt.encode({"user": {'email': user.email, 'role': "Recruiter", 'id': user.id}}, os.getenv('SECRET_KEY'), algorithm=os.getenv('TOKEN_ALGO'))
                    user.token = token
                    db.session.commit()
                
                return successWithData('Login successfully!', {'token': user.token, 'email': user.email})                   
                    
            else:
                return fail('Invalid email or password!'), 401
        else:
            return fail('Email is require!'), 404
    except Exception as e:
        return fail(str(e)), 401
    

# get all
@recruiter_bp.route('/all', methods=['GET'])
def get_all_recruiter():
    try:
        allRecruiter = Recruiter.query.all()
        result =[]
        for each in allRecruiter:
            result.append({
                "id": each.id,
                "name": each.name,
                "email": each.email,
                "company_name": each.company_name,
                "company_address": each.company_address,
                "city": each.city
            })
        return successWithData('All Recruiter', result)
    except Exception as e:
        return fail(str(e)), 401


# update
def update_user(key, user, data):
    if hasattr(user, key):
        setattr(user, key, data[key])

@recruiter_bp.route("/update/<int:id>", methods=['PATCH', 'PUT'])
def udpate_recruiter(id):
    try:
        user = db.session.get(Recruiter, id)
        data = request.get_json()
        if(user):
            for each in data:
                update_user(each, user, data)

            db.session.commit()
            return successWithData("Job Seeker updated successfully!", user)
        else:
            return fail('User not found!'), 404
    except Exception as e:
        return fail(str(e)), 401


#delete
@recruiter_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_recruiter(id):
    try:
        user = db.session.get(Recruiter, id)
        if(user):
            db.session.delete(user)
            db.session.commit()
            return success('User deleted successfully!')
        else:
            return fail("User not found!"), 404
    except Exception as e:
        return fail(str(e)), 401