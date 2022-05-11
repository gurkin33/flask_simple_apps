from flask import request
from flask_restful import Resource

from src.models.user import UserModel


class User(Resource):

    """"
    User resource is CRUD class
    """

    @classmethod
    def get(cls, user_id: int = 0):
        if not user_id:
            return {"error": ["User ID must be present!"]}, 400
        user = UserModel.find_by_id(user_id=user_id)
        if not user:
            return {"error": ["User not found"]}, 404
        return {"user": user.get()}, 200

    @classmethod
    def post(cls):
        user_json = request.get_json()
        v = UserModel.validate(user=user_json)
        if v.failed():
            return {'validation': v.get_messages()}, 400

        new_user = UserModel(**user_json)
        new_user.save()

        return {"user": new_user.get()}, 200

    @classmethod
    def put(cls, user_id: int = 0):
        if not user_id:
            return {"error": ["User ID must be present!"]}, 400
        user = UserModel.find_by_id(user_id=user_id)
        if not user:
            return {"error": ["User not found"]}, 404

        user_json = request.get_json()
        v = UserModel.validate(user=user_json, _id=user_id)
        if v.failed():
            return {'validation': v.get_messages()}, 400

        user.update(data=user_json)
        user.save()

        return {"user": user.get()}, 200

    @classmethod
    def delete(cls, user_id: int = 0):
        if not user_id:
            return {"error": ["User ID must be present!"]}, 400
        user = UserModel.find_by_id(user_id=user_id)
        if not user:
            return {"error": ["User not found"]}, 404

        user.delete()

        return {"result": True}, 200
