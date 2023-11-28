from app import db
from sqlalchemy.sql import func

class SkillSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skills = db.Column(db.String(255))

class GraduateDegree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.Text)

class PostGraduateDegree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.Text)

class JobSeeker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    token = db.Column(db.String(512))
    education = db.Column(db.Text)
    phone = db.Column(db.Integer)
    address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    pincode = db.Column(db.String(10))
    applications = db.relationship('Application', backref='job_seeker_relation', lazy=True)
    skills = db.relationship('SkillSet', secondary='jobseeker_skillset_association', backref='job_seekers', lazy='dynamic')
    graduate = db.relationship('GraduateDegree', secondary='jobseeker_graduatedegree_association', backref='job_seekers', lazy=True)
    postgraduate = db.relationship('PostGraduateDegree', secondary='jobseeker_postgraduatedegree_association', backref='job_seekers', lazy=True)

jobseeker_postgraduatedegree_association = db.Table(
    "jobseeker_postgraduatedegree_association",
    db.Column('jobseeker_id', db.Integer, db.ForeignKey('job_seeker.id')),
    db.Column('postgraduatedegree_id', db.Integer, db.ForeignKey('post_graduate_degree.id'))
)
jobseeker_graduatedegree_association = db.Table(
    "jobseeker_graduatedegree_association",
    db.Column('jobseeker_id', db.Integer, db.ForeignKey('job_seeker.id')),
    db.Column('graduatedegree_id', db.Integer, db.ForeignKey('graduate_degree.id'))
)
jobseeker_skillset_association = db.Table(
    'jobseeker_skillset_association',
    db.Column('jobseeker_id', db.Integer, db.ForeignKey('job_seeker.id')),
    db.Column('skillset_id', db.Integer, db.ForeignKey('skill_set.id'))
)

 
class Recruiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    token = db.Column(db.String(255))
    company_name = db.Column(db.String(255))
    current_jobrole = db.Column(db.String(255))
    company_description = db.Column(db.Text)
    founded = db.Column(db.Integer)
    website = db.Column(db.Text)
    company_size = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    job_postings = db.relationship('JobPosting', backref='recruiter', lazy=True)

class JobPosting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(255))
    description = db.Column(db.Text)
    salary = db.Column(db.String(50))
    graduation = db.Column(db.Text)
    postgraduation = db.Column(db.Text)
    location = db.Column(db.String(255))
    role_category = db.Column(db.String(255)) # Developer, Designer, Analyst
    department = db.Column(db.Text) # Engineering - Software & QA, Sales & Business Development
    experience = db.Column(db.String(50)) # 0-1, 1-2, 2-3
    required_skills = db.Column(db.String(255))
    prefered_skills = db.Column(db.String(255)) 
    employment_type = db.Column(db.String(50)) # part time/full time
    openings = db.Column(db.Integer) # total number of openings
    timestamp = db.Column(db.TIMESTAMP, server_default=func.now())
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'))
    applications = db.relationship('Application', backref='job_posting_relation', lazy=True)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50))
    timestamp = db.Column(db.TIMESTAMP, server_default=func.now())
    job_seeker_id = db.Column(db.Integer, db.ForeignKey('job_seeker.id'))
    job_posting_id = db.Column(db.Integer, db.ForeignKey('job_posting.id'))
    job_posting = db.relationship('JobPosting', backref='applications_relation', lazy=True)
    job_seeker = db.relationship('JobSeeker', backref='applications_relation', lazy=True) 
   
