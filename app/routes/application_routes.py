from flask import Blueprint,  request
from sqlalchemy.orm import joinedload
from app.models import Application,JobSeeker,JobPosting, db
from app import success, fail, successWithData
application_bp = Blueprint('application', __name__)

# apply on job post
@application_bp.route('/apply', methods=['POST'])
def apply_for_job():
    try:
        data = request.get_json()
        user=  request.user
        job_seeker_id = user['id']
        job_posting_id = data.get('job_posting_id')

        if not job_seeker_id or not job_posting_id:
            return fail("Job Seeker ID and Job Posting ID are required"), 400

        job_seeker = JobSeeker.query.get(job_seeker_id)
        job_posting = JobPosting.query.get(job_posting_id)

        if not job_seeker or not job_posting:
            return fail("Job Seeker or Job Posting not found"), 404

        existing_application = Application.query.filter_by(
            job_seeker_id=job_seeker.id,
            job_posting_id=job_posting.id
        ).first()

        if existing_application:
            return fail("Job Seeker has already applied for this job"), 400

        application = Application(
            status=data.get('status', 'Pending'), 
            job_seeker=job_seeker,
            job_posting=job_posting
        )

        db.session.add(application)
        db.session.commit()

        return successWithData("Application submitted successfully!", {"job_id": job_posting_id})

    except Exception as e:
        return fail(str(e)), 500
    
# get all
@application_bp.route('/all', methods=['GET'])
def get_all_applications():
    try:
        applications = Application.query.all()
        result = []

        for application in applications:
            result.append({
                "id": application.id,
                "status": application.status,
                "job_seeker_id": application.job_seeker_id,
                "job_posting_id": application.job_posting_id
            })

        return successWithData("all application",result)

    except Exception as e:
        return fail(str(e)), 401

# get all of single job post
@application_bp.route("/all/<int:jobpost_id>", methods=['GET'])
def get_all_applications_of_job_post(jobpost_id):
    try:
        allApplication = Application.query.filter_by(job_posting_id=jobpost_id).all()
        result = []
        for application in allApplication:
            result.append({
                "id": application.id,
                "status": application.status,
                "job_seeker_id": application.job_seeker_id,
                "job_posting_id": application.job_posting_id
            })

        return successWithData("all application",result)
    except Exception as e:
        return fail(str(e)), 401


#get all of single user(job_seeker)
@application_bp.route("/user/all", methods=['GET'])
def get_all_applications_of_user():
    try:
        job_seeker_id = request.user['id']
        all_application = Application.query.filter_by(job_seeker_id=job_seeker_id).all()
        result = []
        
        for application in all_application:
            result.append({
                "id": application.id,
                "status": application.status,
                "job_seeker_id": application.job_seeker_id,
                "job_posting_id": application.job_posting_id,
                "job_posting": {
                    "id": application.job_posting.id,
                    "job_title": application.job_posting.job_title,
                    "description": application.job_posting.description,
                    "salary": application.job_posting.salary,
                    "graduation":application.job_posting.graduation,
                    "postgraduation":application.job_posting.postgraduation,
                    "location": application.job_posting.location,
                    "role_category": application.job_posting.role_category,
                    "department": application.job_posting.department,
                    "experience": application.job_posting.experience,
                    "required_skills": application.job_posting.required_skills,
                    "prefered_skills": application.job_posting.prefered_skills,
                    "employment_type": application.job_posting.employment_type,
                    "openings": application.job_posting.openings,
                    
                }
            })

        return successWithData(f"all application related to user id {job_seeker_id}",result)
    except Exception as e:
        return fail(str(e)), 401


# update
@application_bp.route('/update/<int:id>', methods=['PATCH', 'PUT'])
def update_application(id):
    try:
        application = Application.query.get(id)
        data = request.get_json()

        if application:
            for key in data:
                setattr(application, key, data[key])

            db.session.commit()
            return successWithData("Job Application updated successfully", application)
        else:
            return fail("Job Application not found!"), 404

    except Exception as e:
        return fail(str(e)), 401

# delete
@application_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_application(id):
    try:
        application = Application.query.get(id)

        if application:
            db.session.delete(application)
            db.session.commit()
            return success("Job Application deleted successfully")
        else:
            return fail("Job Application not found!"), 404

    except Exception as e:
        return fail(str(e)), 401
