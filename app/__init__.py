from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import json
import jwt
from openai import OpenAI
from flask_cors import CORS
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
db = SQLAlchemy(app)
openai_api_key = os.getenv("API_KEY") 
client = OpenAI(api_key=openai_api_key)

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

def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

def serialize_choice(choice):
    res = {
        "message": [serialize_chat_message(message) for message in choice.message],
        "finish_reason": choice.finish_reason,
    }
    return res

def serialize_chat_message(chat_message):
    obj = {
        chat_message[0]: chat_message[1],
    }
    return obj

@app.route("/ai", methods=['POST'])
def getAIOutput():
    try:
        query = request.get_json()
        messages = [{"role": "user", "content": query['query']}]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                },
            }
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            tools=tools,
            tool_choice="auto",  
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        if tool_calls:
           
            available_functions = {
                "get_current_weather": get_current_weather,
            }  
            messages.append(response_message)  
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(
                    location=function_args.get("location"),
                    unit=function_args.get("unit"),
                )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            second_response = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages,
            )  # get a new response from the model where it can see the function response     
            result = {
                "id": second_response.id,
                "choices": [serialize_choice(choice) for choice in second_response.choices],
              
            }      
            return successWithData(msg="second output", data=result)
        else:
            return successWithData(msg="output", data = response_message)
    except Exception as e:
        return fail(str(e))

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