from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

find_picture_by_id = lambda id: next((pic for pic in data if pic['id'] == id), None)

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    res = find_picture_by_id(id)
    status_code = 200 if res else 404
    return jsonify(res), status_code


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.json
    if not picture:
        return jsonify(Message="Invalid input parameter"), 422
    elif find_picture_by_id(picture['id']):
        return jsonify(Message=f"picture with id {picture['id']} already present"), 302
    
    try:
        data.append(picture)
    except Exception:
        return {"Message": "data not defined"}, 500

    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    payload = request.json
    
    if not payload:
        return jsonify(Message="Invalid input parameter"), 422

    picture = find_picture_by_id(id)
    
    if not picture:
        return jsonify(Message="picture not found"), 404
    
    try:
        for k,v in payload.items():
            picture[k] = v
        
    except Exception:
        return {"Message": "data not defined"}, 500

    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture = find_picture_by_id(id)
    if not picture:
        return jsonify(Message="picture not found"), 404
    
    try:
        data.remove(picture)
    except Exception:
        return {"Message": "data not defined"}, 500

    return jsonify(picture), 204
