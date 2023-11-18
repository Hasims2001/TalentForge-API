from flask import Blueprint, jsonify, request
from app.models import JobPosting, db
from app import success, fail, successWithData
jobposting_bp = Blueprint('jobposting', __name__)

# create a new 
@jobposting_bp.route('/create', methods=['POST'])
def create_jobposting():
    try:
        data = request.get_json()
        user = request.user
        new_jobposting = JobPosting(
            job_title=data['job_title'],
            description=data['description'],
            salary=data['salary'],
            skills=data['skills'],
            qualification=data['qualification'],
            location=data['location'],
            role_category=data['role_category'],
            department=data['department'],
            experience=data['experience'],
            required_skills=data['required_skills'],
            employment_type=data['employment_type'],
            company_name=data['company_name'],
            company_info=data['company_info'],
            openings=data['openings'],
            recruiter_id=user.id
        )

        db.session.add(new_jobposting)
        db.session.commit()

        return successWithData("Job post created successfully!", new_jobposting)

    except Exception as e:
        return fail(str(e)), 401

# get all 
@jobposting_bp.route('/all', methods=['GET'])
def get_all_jobpostings():
    try:
        jobpostings = JobPosting.query.all()
        result = []
        user = request.user
        for jobposting in jobpostings:
            result.append({
                "id": jobposting.id,
                "job_title": jobposting['job_title'],
                "description": jobposting['description'],
                "salary": jobposting['salary'],
                "skills": jobposting['skills'],
                "qualification": jobposting['qualification'],
                "location": jobposting['location'],
                "role_category": jobposting['role_category'],
                "department": jobposting['department'],
                "experience": jobposting['experience'],
                "required_skills": jobposting['required_skills'],
                "employment_type": jobposting['employment_type'],
                "company_name": jobposting['company_name'],
                "company_info": jobposting['company_info'],
                "openings": jobposting['openings'],
                "recruiter_id": user.id
            })

        return successWithData("all jobs", result)

    except Exception as e:
        return fail(str(e)), 401

@jobposting_bp.route('/update/<int:id>', methods=['PATCH', 'PUT'])
def update_jobposting(id):
    try:
        jobposting = db.session.get(JobPosting, id)
        data = request.get_json()

        if jobposting:
            for key in data:
                setattr(jobposting, key, data[key])

            db.session.commit()
            return successWithData('Job post updated successfully!', jobposting)
        else:
            return fail("Job post not found!"), 404

    except Exception as e:
        return fail(str(e)), 401

#  delete 
@jobposting_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_jobposting(id):
    try:
        jobposting = db.session.get(JobPosting, id)
        if jobposting:
            db.session.delete(jobposting)
            db.session.commit()
            return success("Job Posting deleted successfully")
        else:
            return fail("Job post not found!"), 404

    except Exception as e:
        return fail(str(e)), 401
