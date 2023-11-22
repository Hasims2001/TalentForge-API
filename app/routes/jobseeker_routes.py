from flask import Blueprint, request
from app.models import JobSeeker, db
import jwt
import os
from passlib.hash import pbkdf2_sha256
from app import success, fail, successWithData
from dotenv import load_dotenv
jobseeker_bp = Blueprint('jobseeker', __name__)
load_dotenv()


# new 
@jobseeker_bp.route('/register', methods=['POST'])
def register_jobseeker():
    try:
        data = request.get_json()
        hashed = pbkdf2_sha256.using(rounds=10, salt_size=16).hash(data['password'])
        new_jobseeker = JobSeeker(
            name=data['name'],
            email=data['email'],
            password=hashed,
            token="",
            education=data['education'] if 'education' in data else "",
            address=data['address'],
            city=data['city'],
            state=data['state'],
            pincode=data['pincode']
        )

        db.session.add(new_jobseeker)
        db.session.commit()

        return success("Register successfully!")
    except Exception as e:
        return fail(str(e)), 500

# login
@jobseeker_bp.route('/login', methods=['POST'])
def login_jobseeker():
    try:
        data = request.get_json()
        user = JobSeeker.query.filter_by(email=data['email']).first()
        
        if(user and pbkdf2_sha256.verify(data['password'], user.password)):
            if(user.token == ""):
                token = jwt.encode({"user": {'email': user.email, 'role': "Jobseeker", 'id': user.id}}, os.getenv('SECRET_KEY'), algorithm=os.getenv('TOKEN_ALGO'))  
                user.token = token
                db.session.commit()
            
            result = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": "Jobseeker",
                "token": user.token,
                "address": user.address,
                "city": user.city,
                "state": user.state,
                "pincode": user.pincode,

            }

            return successWithData('Login successfully!', result)                   
                    
        else:
            return fail('Invalid email or password!'), 401
     
    except Exception as e:
        return fail(str(e)), 401

# get all
@jobseeker_bp.route('/all', methods=['GET'])
def get_all_jobseekers():
    try:
        jobseekers = JobSeeker.query.all()
        result = []

        for each in jobseekers:
            result.append({
                "id": each.id,
                "name": each.name,
                "email": each.email,
                "skills": each.skills,
                "city": each.city
            })

        return successWithData("All jobseekers",result)
    except Exception as e:
        return fail(str(e)), 401

# get
@jobseeker_bp.route('/<int:id>', methods=['GET'])
def get_jobseeker(id):
    try:
        user = db.session.get(JobSeeker, id)
        result = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "education": user.education,
                "skills": user.skills,
                "city": user.city,
                "state": user.state
            }

        return successWithData(f"jobseeker id {id}",result)
    except Exception as e:
        return fail(str(e)), 401


# update 
@jobseeker_bp.route('/update/<int:id>', methods=['PATCH', "PUT"])
def update_jobseeker(id):
    try:
        user = db.session.get(JobSeeker, id)
        data = request.get_json()

        if(user):
            for each in data:
                setattr(user, each, data[each])

            db.session.commit()
            return successWithData("Job Seeker updated successfully!", user)
        else:
            return fail("User not found!"), 404
           
    except Exception as e:
        return fail(str(e)), 401


# delete 
@jobseeker_bp.route("/delete/<int:id>", methods=['DELETE'])
def delete_jobseeker(id):
    try:
        user = db.session.get(JobSeeker, id)
        if(user):
            db.session.delete(user)
            db.session.commit()
            return success('User deleted successfully!')
    except Exception as e:
        return fail(str(e)), 401