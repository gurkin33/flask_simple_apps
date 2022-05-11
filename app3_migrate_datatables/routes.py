from flask_restful import Api
from src.resources import User, UserTable


class RouteMaker:

    _routes = [
        (User, '/user', '/user/<int:user_id>'),
        (UserTable, '/user/table')
    ]

    @classmethod
    def run(cls, api: Api):
        for r in cls._routes:
            api.add_resource(*r)
