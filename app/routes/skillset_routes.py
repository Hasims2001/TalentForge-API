from flask import Blueprint, jsonify, request
from app.models import SkillSet, db
from app import success, fail, successWithData
skillset_bp = Blueprint('skillset', __name__)

# create
@skillset_bp.route('/create', methods=['POST'])
def create_skillset():
    try:
        data = request.get_json()

        new_skillset = SkillSet(
            skills=data['skills']
        )
        db.session.add(new_skillset)
        db.session.commit()

        return success("Skill Set created successfully")
    except Exception as e:
        return fail(str(e)), 401

# get all 
@skillset_bp.route('/all', methods=['GET'])
def get_all_skillsets():
    try:
        skillsets = SkillSet.query.all()
        result = []

        for skillset in skillsets:
            result.append({
                "id": skillset.id,
                "skills": skillset.skills
            })

        return successWithData("all skills",result)

    except Exception as e:
        return fail(str(e)), 401

# get
@skillset_bp.route("/<int:id>", methods=['GET'])
def get_skill(id):
    try:
        skill =db.session.get(SkillSet, id)
        if(skill):
            return successWithData("skill", skill)
        else:
            return fail("Skill Set not found!"), 404
    except Exception as e:
        return fail(str(e)), 401

# update 
@skillset_bp.route('/update/<int:id>', methods=['PATCH', 'PUT'])
def update_skillset(id):
    try:
        skillset = db.session.get(SkillSet, id)
        data = request.get_json()

        if skillset:
            for key in data:
                setattr(skillset, key, data[key])

            db.session.commit()
            return successWithData("Skill Set updated successfully", skillset)
        else:
            return fail("Skill Set not found!"), 404

    except Exception as e:
        return fail(str(e)), 401

#  delete
@skillset_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_skillset(id):
    try:
        skillset =db.session.get(SkillSet, id)

        if skillset:
            db.session.delete(skillset)
            db.session.commit()
            return success("Skill Set deleted successfully")
        else:
            return fail("Skill Set not found!"), 404

    except Exception as e:
        return fail(str(e)), 401
