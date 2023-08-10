"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#1/ALL MEMBERS
@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }

    return jsonify(response_body), 200

# 2/ONE MEMBER
@app.route('/member/<int:member_id>', methods=['GET'])
def handle_member(member_id):

    member = jackson_family.get_member(member_id)

    if member:
        response_body = {
            "member": member
        }
        return jsonify(response_body), 200
    else:
        response_body = {
            "error": "Member not found"
        }
        return jsonify(response_body), 404

#3/CREATE ONE MEMBER
@app.route('/members/', methods=['POST'])
def handle_create():
    
    request_body = request.get_json(force=True)
    if "first_name" not in request_body or "age" not in request_body or "lucky_numbers" not in request_body:
        response_body = {
            "error": "Incomplete data"
        }
        return jsonify(response_body), 400
    else:
        jackson_family.add_member(request_body)

    response_body = {
        "msg": "Member created"
    }

    return jsonify(response_body), 200


#4/ DELETE ONE MEMBER
@app.route('/delete/<int:member_id>', methods=['DELETE'])
def handle_delete(member_id):

    if jackson_family.delete_member(member_id):
        response_body = {
            "msg": "Member deleted"
        }
        return jsonify(response_body), 200
    else:
        response_body = {
            "error": "Member not found"
        }
        return jsonify(response_body), 404

#UPDATE ONE MEMBER
@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    request_data = request.get_json()
    updated_member = {
        "id": member_id,
        "first_name": request_data["first_name"],
        "last_name": jackson_family.last_name,
        "age": request_data["age"],
        "lucky_numbers": request_data["lucky_numbers"]
    }
    if jackson_family.update_member(member_id, updated_member):
        return jsonify({"message": "Member updated successfully"}), 200
    else:
        return jsonify({"message": "Member not found"}), 404



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)