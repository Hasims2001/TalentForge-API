from app import db

class JobSeeker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    token = db.Column(db.String(512))
    skills = db.Column(db.String(255))
    address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    pincode = db.Column(db.String(10))

class Recruiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    token = db.Column(db.String(255))
    company_name = db.Column(db.String(255))
    company_address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    pincode = db.Column(db.String(10))

class JobPosting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(255))
    description = db.Column(db.Text)
    salary = db.Column(db.String(50))
    skills = db.Column(db.String(255))
    qualification = db.Column(db.String(255))
    location = db.Column(db.String(255))
    role_category = db.Column(db.String(255))
    department = db.Column(db.String(255))
    experience = db.Column(db.String(50))
    required_skills = db.Column(db.String(255))
    employment_type = db.Column(db.String(50))
    company_name = db.Column(db.String(255))
    company_info = db.Column(db.Text)
    openings = db.Column(db.Integer)
    timestamp = db.Column(db.TIMESTAMP)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'))
    recruiter = db.relationship('Recruiter', backref=db.backref('jobpostings', lazy=True))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50))
    timestamp = db.Column(db.TIMESTAMP)

class SkillSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skills = db.Column(db.String(255))
