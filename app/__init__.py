from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import jwt
from flask_cors import CORS
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
db = SQLAlchemy(app)


from app.models import SkillSet, JobSeeker, Recruiter, JobPosting, Application, jobseeker_skillset_association
with app.app_context():
    db.create_all()

CORS(app, origins="http://localhost:3000")

def success(msg):
    return jsonify({'issue': False, 'message': msg})

def successWithData(msg, data):
    return jsonify({'issue': False, 'message': msg, 'data': data})

def fail(msg):
    return jsonify({'issue': True, 'message': msg})

def authenticate_token():
    excluded_endpoints = [ "Documentation", 'jobseeker.register_jobseeker', "jobseeker.login_jobseeker", "recruiter.register_recruiter", "recruiter.login_recruiter"]
    if request.endpoint in excluded_endpoints:
        return 
    
    try:
        token = request.headers.get('Authorization')
        if(token):
            decoded_token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('TOKEN_ALGO')])
            request.user =  decoded_token['user']
        else:
            return fail('Token not found')
    except Exception as e:
        return fail(str(e)), 401


     

@app.route("/", methods=["GET"])
def Documentation():
    return success("Welcome to TalentForge")

app.before_request(authenticate_token)
from app.routes.jobseeker_routes import jobseeker_bp
from app.routes.recruiter_routes import recruiter_bp
from app.routes.jobposting_routes import jobposting_bp
from app.routes.application_routes import application_bp
from app.routes.skillset_routes import skillset_bp
app.register_blueprint(jobseeker_bp, url_prefix='/jobseeker')
app.register_blueprint(recruiter_bp, url_prefix="/recruiter")
app.register_blueprint(jobposting_bp, url_prefix="/jobposting")
app.register_blueprint(application_bp, url_prefix="/application")
app.register_blueprint(skillset_bp, url_prefix="/skillset")