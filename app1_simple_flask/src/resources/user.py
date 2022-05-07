import random
from flask_restful import Resource


class User(Resource):

    """"
    User resource is CRUD class
    """

    @classmethod
    def get(cls, user_id: int = 0):
        if not user_id:
            return {"error": ["User ID must be present!"]}, 400
        return {"user": {"id": user_id}}, 200

    @classmethod
    def post(cls):
        return {"user": {"id": random.randint(1, 100)}}, 200

    @classmethod
    def put(cls, user_id: int = 0):
        if not user_id:
            return {"error": ["User ID must be present!"]}, 400
        return {"user": {"id": user_id}}, 200

    @classmethod
    def delete(cls, user_id: int = 0):
        if not user_id:
            return {"error": ["User ID must be present!"]}, 400
        return {"result": True}, 200
