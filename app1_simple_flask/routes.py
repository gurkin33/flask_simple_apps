from flask_restful import Api
from src.resources.user import User


class RouterGenerator:

    _routes = [
        (User, '/user', '/user/<int:user_id>')
    ]

    @classmethod
    def run(cls, api: Api):
        for r in cls._routes:
            api.add_resource(*r)
