from flask import Blueprint


jobseeker_bp = Blueprint('jobseeker', __name__)
recruiter_bp = Blueprint('recruiter', __name__)
jobposting_bp = Blueprint('jobposting', __name__)
application_bp = Blueprint('application', __name__)
# skillset_bp = Blueprint('skillset', __name__)


from . import jobseeker_routes, recruiter_routes,jobposting_routes, application_routes
#, skillset_routes

# routes with their respective blueprints
jobseeker_bp.register_blueprint(jobseeker_routes.jobseeker_bp)
recruiter_bp.register_blueprint(recruiter_routes.recruiter_bp)
jobposting_bp.register_blueprint(jobposting_routes.jobposting_bp)
application_bp.register_blueprint(application_routes.application_bp)
# skillset_bp.register_blueprint(skillset_routes.skillset_bp)
