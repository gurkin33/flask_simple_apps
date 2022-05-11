from flask import request

from src.models.user import UserModel
from src import ResourceCustom


class UserTable(ResourceCustom):

    """"
    User table resource is CRUD class
    """

    # @classmethod
    # def get(cls):
    #     td = request.args
    #     return td

    @classmethod
    def post(cls):
        td = request.get_json()

        #  method of ResourceCustom
        return cls.datatables(model=UserModel, req=td)
