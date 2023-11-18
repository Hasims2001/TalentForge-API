from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import jwt
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
db = SQLAlchemy(app)

def success(msg):
    return jsonify({'issue': False, 'message': msg})

def successWithData(msg, data):
    return jsonify({'issue': False, 'message': msg, 'data': data})

def fail(msg):
    return jsonify({'issue': True, 'message': msg})

def authenticate_token():
    excluded_endpoints = ['/login', "/register"]
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

app.register_blueprint(jobseeker_bp, url_prefix='/jobseeker')

with app.app_context():
    db.create_all()