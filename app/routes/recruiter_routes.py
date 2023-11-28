from flask import Blueprint, request, jsonify
from app.models import Recruiter,JobPosting,Application, db
import jwt
import os
from passlib.hash import pbkdf2_sha256
from app import success, fail, successWithData
from dotenv import load_dotenv
recruiter_bp = Blueprint('recruiter', __name__)
load_dotenv()

# model
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(255))
    # email = db.Column(db.String(255), unique=True)
    # password = db.Column(db.String(255))
    # token = db.Column(db.String(255))
    # company_name = db.Column(db.String(255))
    # current_jobrole = db.Column(db.String(255))
    # company_description = db.Column(db.Text)
    # founded = db.Column(db.Integer)
    # website = db.Column(db.Text)
    # company_size = db.Column(db.String(255))
    # city = db.Column(db.String(255))
    # state = db.Column(db.String(255))
    # job_postings = db.relationship('JobPosting', backref='recruiter', lazy=True)

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
            current_jobrole=data['current_jobrole'],
            company_description= data.get('company_description', ""),
            founded= data.get("founded", 0000),
            website=data.get('website', ""),
            company_size=data.get("company_size", ""),
            city=data['city'],
            state=data['state'],
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
                
                result = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": "Recruiter",
                    "token": user.token,
                    "company_name": user.company_name,
                    "current_jobrole": user.current_jobrole,
                    "company_description": user.company_description,
                    "founded": user.founded,
                    "website": user.website,
                    "company_size": user.company_size,
                    "city": user.city,
                    "state": user.state,

                }
                return successWithData('Login successfully!', result)                   
                    
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
                "current_jobrole": each.current_jobrole,
                "company_description": each.company_description,
                "founded": each.founded,
                "website": each.website,
                "company_size": each.company_size,
                "city": each.city,
                "state": each.state,
            })
        return successWithData('All Recruiter', result)
    except Exception as e:
        return fail(str(e)), 401

# get
@recruiter_bp.route("/<int:id>", methods=['GET'])
def get_recruiter(id):
    try:
        user = db.session.get(Recruiter, id)
        result = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'company_name': user.company_name,
            'current_jobrole': user.current_jobrole,
            'company_description': user.company_description,
            'founded': user.founded,
            'website': user.website,
            'company_size': user.company_size,
            'city': user.city,
            "state": user.state,
        }
        return successWithData(f'Recruiter id {id}', result)
    except Exception as e:
        return fail(str(e)), 401
    
    
# update
@recruiter_bp.route("/update/<int:id>", methods=['PATCH', 'PUT'])
def udpate_recruiter(id):
    try:
        user = db.session.get(Recruiter, id)
        data = request.get_json()
        if(user):
            for each in data:
                setattr(user, each, data[each])

            db.session.commit()
            result = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'company_name': user.company_name,
                'current_jobrole': user.current_jobrole,
                'company_description': user.company_description,
                'founded': user.founded,
                'website': user.website,
                'company_size': user.company_size,
                'city': user.city,
                "state": user.state,
            }
            return successWithData("Job Seeker updated successfully!", result)
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
    

# get all applications for single job post
@recruiter_bp.route('/applications/<int:job_posting_id>', methods=['GET'])
def get_job_posting_applications(job_posting_id):
    try:
        job_posting = JobPosting.query.get(job_posting_id)

        if not job_posting:
            return fail("Job Posting not found"), 404

        applications = Application.query.filter_by(job_posting_id=job_posting.id).all()

        application_data = []
        for application in applications:
            user_skills = application.job_seeker.skills
            user_skills = [skill.skills for skill in user_skills]
            temp_graduate = application.job_seeker.graduate
            user_graduate = [degree.degree for degree in temp_graduate]
            temp_postgraduate = application.job_seeker.postgraduate
            user_postgraduate = [degree.degree for degree in temp_postgraduate]

            application_data.append({
                "id": application.id,
                "status": application.status,
                "timestamp": application.timestamp,
                "job_posting_id": application.job_posting_id,
                "job_seeker": {
                    "id": application.job_seeker.id,
                    "name": application.job_seeker.name,
                    "email": application.job_seeker.email,
                    "city": application.job_seeker.city,
                    "state": application.job_seeker.state,
                    "user_skills": user_skills,
                    "education": application.job_seeker.education,
                    "graduate": user_graduate,
                    "postgraduate": user_postgraduate,
                }
            })

        return successWithData("Applications retrieved successfully!", application_data)

    except Exception as e:
        return fail(str(e)), 500
    
# update application status of single job post
@recruiter_bp.route("/applications/<int:application_id>", methods=['PATCH', 'PUT'])
def udpate_application_status(application_id):
    try:
        application = Application.query.get(application_id)
        data = request.get_json()

        if application:
            for key in data:
                setattr(application, key, data[key])

            db.session.commit()
            user_skills = application.job_seeker.skills
            user_skills = [skill.skills for skill in user_skills]
            temp_graduate = application.job_seeker.graduate
            user_graduate = [degree.degree for degree in temp_graduate]
            temp_postgraduate = application.job_seeker.postgraduate
            user_postgraduate = [degree.degree for degree in temp_postgraduate]
            result = {
                    "id": application.id,
                    "status": application.status,
                    "timestamp": application.timestamp,
                    "job_posting_id": application.job_posting_id,
                    "job_seeker": {
                        "id": application.job_seeker.id,
                        "name": application.job_seeker.name,
                        "email": application.job_seeker.email,
                        "city": application.job_seeker.city,
                        "state": application.job_seeker.state,
                        "user_skills": user_skills,
                        "education": application.job_seeker.education,
                        "graduate": user_graduate,
                        "postgraduate": user_postgraduate,
                    }
            }
            return successWithData("Application status updated successfully", result)
        else:
            return fail("Application not found!"), 404
    except Exception as e:
        return fail(str(e)), 401


   