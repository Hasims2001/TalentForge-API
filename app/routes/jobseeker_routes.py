from flask import Blueprint, jsonify, request
from app.models import JobSeeker, db
import json
import jwt
import os
from passlib.hash import pbkdf2_sha256
from app import success, fail, successWithData
from dotenv import load_dotenv
jobseeker_bp = Blueprint('jobseeker', __name__)
load_dotenv()
# new Job Seeker
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
            skills=data['skills'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            pincode=data['pincode']
        )

        db.session.add(new_jobseeker)
        db.session.commit()

        return success("Register successfully!")
    except Exception as e:
        return fail(str(e)), 401

# login Job Seeker
@jobseeker_bp.route('/login', methods=['POST'])
def login_jobseeker():
    try:
        data = request.get_json()
        if 'email' in data:
            user = JobSeeker.query.filter_by(email=data['email']).first()
            if(user and pbkdf2_sha256.verify(data['password'], user.password)):
                if(user.token == ""):
                    token = jwt.encode({"user": {'email': user.email, 'role': "Jobseeker", 'name': user.name}}, os.getenv('SECRET_KEY'), algorithm=os.getenv('TOKEN_ALGO'))
                    user.token = token
                    db.session.commit()
                
                return successWithData('Login successfully!', {'token': user.token, 'email': user.email})                   
                    
            else:
                return fail('email or password is wrong!'), 401
        else:
            return fail('email is require!'), 401
    except Exception as e:
        return fail(str(e)), 401

# get all Job Seekers
@jobseeker_bp.route('/all', methods=['GET'])
def get_all_jobseekers():
    try:
        jobseekers = JobSeeker.query.all()
        result = []

        for jobseeker in jobseekers:
            result.append({
                "id": jobseeker.id,
                "name": jobseeker.name,
                "email": jobseeker.email,
                "skills": jobseeker.skills,
                "city": jobseeker.city
            })

        return successWithData("All jobseekers",result)
    except Exception as e:
        return fail(str(e)), 401


# update Job Seekers
def update_user(key, user, data):
    if hasattr(user, key):
        setattr(user, key, data[key])

@jobseeker_bp.route('/update/<int:id>', methods=['PATCH', "PUT"])
def update_jobseeker(id):
    try:
        user = db.session.get(JobSeeker, id)
        data = request.get_json()

        if(user):
            for each in data:
                update_user(each, user, data)

            db.session.commit()
            return successWithData("Job Seeker updated successfully!", user)
        else:
            return fail("Jobseeker not found!")
           
    except Exception as e:
        return fail(str(e)), 401


# delete Job Seekers
@jobseeker_bp.route("/delete/<int:id>", methods=['DELETE'])
def delete_jobseeker(id):
    try:
        user = db.session.get(JobSeeker, id)
        if(user):
            db.session.delete(user)
            db.session.commit()
            return success('Deleted successfully!')
    except Exception as e:
        return fail(str(e)), 401