from flask import Blueprint, request
from app.models import JobSeeker, SkillSet,GraduateDegree,PostGraduateDegree,JobPosting, Application, db
import jwt
import os
import json
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
            phone= data['phone'],
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
                "phone": user.phone,
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
            user_skills = [skill.skills for skill in each.skills]
            result.append({
                "id": each.id,
                "name": each.name,
                "email": each.email,
                "graduate": each.graduate,
                "postgraduate": each.postgraduate,
                "education": each.education,
                "skills": user_skills,
                "city": each.city,
                "state": each.state,
                'pincode': each.pincode

            })

        return successWithData("All jobseekers",result)
    except Exception as e:
        return fail(str(e)), 401

# get
@jobseeker_bp.route('/<int:id>', methods=['GET'])
def get_jobseeker(id):
    try:
        user = db.session.get(JobSeeker, id)
        if(user):
            user_skills = [skill.skills for skill in user.skills]
            result = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "education": user.education,
                    "graduate": user.graduate,
                    "postgraduate": user.postgraduate,
                    "user_skills": user_skills,
                    "phone": user.phone,
                    "city": user.city,
                    "state": user.state,
                    'pincode': user.pincode
                }

            return successWithData(f"jobseeker id {id}",result)
        else:
            return fail('User not found!'), 404
    except Exception as e:
        return fail(str(e)), 401


# update 
@jobseeker_bp.route('/update/<int:id>', methods=['PATCH', "PUT"])
def update_jobseeker(id):
    try:
        user = db.session.get(JobSeeker, id)
        data = request.get_json()
        
        if(user):
            for key, value in data.items():
                if key == "skills":
                    update_user_skills(user, value)
                elif key == "graduate":
                    update_user_graduate(user, value)
                elif key == "postgraduate":
                    update_user_postgraduate(user, value)
                elif key == "password":
                    hashed = pbkdf2_sha256.using(rounds=10, salt_size=16).hash(value)
                    setattr(user, key, hashed)
                else:
                    setattr(user, key, value)

            
            db.session.commit()
            user_skills = [skill.skills for skill in user.skills]
            user_graduate = [degree.degree for degree in user.graduate]
            user_postgraduate = [degree.degree for degree in user.postgraduate]
            result = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "education": user.education,
                "graduate": user_graduate,
                "postgraduate": user_postgraduate,
                "skills": user_skills,
                "phone": user.phone,
                "city": user.city,
                "state": user.state,
                "pincode": user.pincode
            }
            return successWithData("Job Seeker updated successfully!", result)
        else:
            return fail("User not found!"), 404
           
    except Exception as e:
        return fail(str(e)), 401

def update_user_skills(user, new_skills):
    user.skills = []

    for skill_name in new_skills:
        skill = SkillSet.query.filter_by(skills=skill_name).first()
        if skill is None:
            skill = SkillSet(skills=skill_name)
            db.session.add(skill)
        user.skills.append(skill)


def update_user_graduate(user, new_graduate):
    degree_name = GraduateDegree.query.filter_by(degree=new_graduate).first()
    
    if degree_name is None:
        degree_name = GraduateDegree(degree=new_graduate)
        db.session.add(degree_name)
    user.graduate.append(degree_name)
    
    
def update_user_postgraduate(user, new_postgraduate):
    degree_name = PostGraduateDegree.query.filter_by(degree=new_postgraduate).first()
    if degree_name is None:
        degree_name = PostGraduateDegree(degree=new_postgraduate)
        db.session.add(degree_name)
    user.postgraduate.append(degree_name)


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
    
