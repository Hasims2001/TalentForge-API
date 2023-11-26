from app import app


if __name__ == "__main__":
    app.run(debug=True)

# job_portal/
# |-- app/
# |   |-- __init__.py
# |   |-- models.py
# |   |-- routes/
# |   |   |-- __init__.py
# |   |   |-- jobseeker_routes.py
# |   |   |-- recruiter_routes.py
# |   |   |-- jobposting_routes.py
# |   |   |-- application_routes.py
# |   |   |-- skillset_routes.py
# |-- migrations/
# |-- venv/
# |-- config.py
# |-- run.py