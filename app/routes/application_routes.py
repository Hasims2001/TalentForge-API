from flask import Blueprint,  request
from app.models import Application, db
from app import success, fail, successWithData
application_bp = Blueprint('application', __name__)

# create 
@application_bp.route('/create', methods=['POST'])
def create_application():
    try:
        data = request.get_json()
        user = request.user
        new_application = Application(
            status=data['status'],
            job_seeker_id=user.id,
            job_posting_id=data['job_posting_id']
        )

        db.session.add(new_application)
        db.session.commit()

        return success("Applied successfully!")

    except Exception as e:
        return fail(str(e)), 401

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
