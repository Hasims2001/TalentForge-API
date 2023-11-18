from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
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

@app.route("/", methods=["GET"])
def Documentation():
    return success("Welcome to TalentForge")

from app.routes.jobseeker_routes import jobseeker_bp

app.register_blueprint(jobseeker_bp, url_prefix='/jobseeker')

with app.app_context():
    db.create_all()