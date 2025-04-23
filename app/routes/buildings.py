from flask import Blueprint, jsonify, abort, make_response, request
from app.services import (
    get_all_buildings,
    get_building_by_id,
    insert_building,
    update_building_by_id,
    delete_building_by_id,
)
from app.auth import auth
from app.serializers import buildings_cschema, building_cschema

building_bp = Blueprint("main", __name__)


@building_bp.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@building_bp.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad Request"}), 400)


@building_bp.route("/")
@auth.login_required
def hello_world():
    return jsonify({"app": "Самые высокие здания и сооружения"})


@building_bp.route("/buildings", methods=["GET"])
@auth.login_required
def get_structures():
    buildings = get_all_buildings()
    return jsonify({"buildings": buildings_cschema.dump(buildings)})


@building_bp.route("/buildings/<int:id>", methods=["GET"])
@auth.login_required
def get_building(id):
    building = get_building_by_id(id)
    if building is None:
        abort(404)
    return jsonify({"buildings": building_cschema.dump(building)})


@building_bp.route("/buildings", methods=["POST"])
@auth.login_required
def create_building():
    if (
        not request.json
        or "title" not in request.json
        or "type_building_id" not in request.json
        or "city_id" not in request.json
    ):
        abort(400)
    new_building = request.get_json()
    if "height" not in request.json:
        new_building["height"] = 0
    if "year" not in request.json:
        new_building["year"] = 2000

    building_new = insert_building(new_building)
    return jsonify({"building": building_cschema.dump(building_new)}), 201


@building_bp.route("/buildings/<int:id>", methods=["PUT"])
@auth.login_required
def update_building(id):
    building = get_building(id)
    if building is None or not request.json:
        abort(404)
    if "title" in request.json and type(request.json["title"]) is not str:
        abort(400)
    if (
        "type_building_id" in request.json
        and type(request.json["type_building_id"]) is not int
    ):
        abort(400)
    if "city_id" in request.json and type(request.json["city_id"]) is not int:
        abort(400)
    if "year" in request.json and type(request.json["year"]) is not int:
        abort(400)
    if "height" in request.json and type(request.json["height"]) is not int:
        abort(400)
    building_update = update_building_by_id(id, request.get_json())
    return jsonify({"building": building_cschema.dump(building_update)})


@building_bp.route("/buildings/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_one_building(id):
    building = get_building(id)
    if building is None:
        abort(404)

    delete_building_by_id(id)
    return jsonify({"result": True})
