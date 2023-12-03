# TalentForge API (Flask App)

Welcome to Talent Forge, Our cutting-edge job matching platform leverages the power of GenAI integration, empowering recruiters to effortlessly connect with ideal candidates and enabling job seekers to discover tailored opportunities aligned with their unique skills and experience. Transform your hiring process and career journey with Talent Forge today!

Built using Flask app and integret MySQL as database.

## Table of Contents

- [Folder Structure](#Folder-Structure)
- [Tech Stack](#Tech-Stack)
- [Links](#Links)
- [Database Schema](#Database-Schema)
- [Installation](#installation)

### Folder-Structure

TalentForge-API/
|-- app/
| |-- **init**.py
| |-- models.py
| |-- routes/
| | |-- **init**.py
| | |-- jobseeker_routes.py
| | |-- recruiter_routes.py
| | |-- jobposting_routes.py
| | |-- application_routes.py
| | |-- skillset_routes.py
|-- venv/
|-- run.py

### Links:

- Website: [Telent Forge](https://talent-forge-one.vercel.app/)
- Frontend Repo: [Github](https://github.com/Hasims2001/TalentForge)

### Tech Stack

- Flask
- MySQL

### Database Schema

<table>
<tr>
<th>Table</th>
<th>Fields</th>
</tr>
<tr>
<td>Jobseeker</td>
 <td>
    id (integer),
      name (string),
      email (string, unique),
      password (string),
      token (string),
      education (text),
      experience (text),
      phone (integer),
      address (string),
      city (string),
      state (string),
      pincode (string),
      applications (relationship with 'Application'),
      skills (relationship with 'SkillSet'),
      graduate (relationship with 'GraduateDegree'),
      postgraduate (relationship with 'PostGraduateDegree')
    </td>
</tr>
 <tr>
    <td>Recruiter</td>
    <td>
      id (integer),
      name (string),
      email (string, unique),
      password (string),
      token (string),
      company_name (string),
      current_jobrole (string),
      company_logo (text),
      company_description (text),
      founded (integer),
      website (text),
      company_size (string),
      city (string),
      state (string),
      job_postings (relationship with 'JobPosting')
    </td>
  </tr>
 <tr>
    <td>JobPosting</td>
    <td>
      id (integer),
      job_title (string),
      description (text),
      salary (string),
      graduation (text),
      postgraduation (text),
      location (string),
      role_category (string),
      department (text),
      experience (string),
      required_skills (string),
      prefered_skills (string),
      employment_type (string),
      openings (integer),
      timestamp (timestamp with default),
      recruiter_id (integer, foreign key to 'Recruiter'),
      applications (relationship with 'Application')
    </td>
  </tr>
 <tr>
    <td>Application</td>
    <td>
      id (integer),
      status (string),
      timestamp (timestamp with default),
      job_seeker_id (integer, foreign key to 'JobSeeker'),
      job_posting_id (integer, foreign key to 'JobPosting'),
      job_posting (relationship with 'JobPosting'),
      job_seeker (relationship with 'JobSeeker')
    </td>
  </tr>
</table>

### Installation

Python should be installed before going to next step.

open folder where you want to install the app.

paste the below line into terminal(cmd)

```
git clone https://github.com/Hasims2001/TalentForge-API.git
```

run this command in terminal

```
pip install -r requirements.txt
```

finally,

```
python run.py
```
