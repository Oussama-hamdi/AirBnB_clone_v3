#!/usr/bin/python3
"""RESTful API actions for Review objects"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_reviews_by_place(place_id):
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    review_list = [rev.to_dict() for rev in place.reviews]
    return jsonify(review_list), 200


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review_by_id(review_id):
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    if storage.get("Place", place_id) is None:
        abort(404)
    elif not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "user_id" not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    elif storage.get("User", request.get_json()["user_id"]) is None:
        abort(404)
    elif "text" not in request.get_json():
        return jsonify({"error": "Missing text"}), 400
    else:
        obj_data = request.get_json()
        obj = Review(**obj_data)
        obj.place_id = place_id
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review_by_id(review_id):
    obj = storage.get("Review", review_id)

    if obj is None:
        abort(404)
    elif not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    else:
        obj_data = request.get_json()
        ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]

        for key in obj_data.keys():
            if key in ignore_keys:
                pass
            else:
                setattr(obj, key, obj_data[key])

        obj.save()
        return jsonify(obj.to_dict()), 200
