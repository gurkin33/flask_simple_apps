from typing import Dict, Any

from db import db
from respect_validation import Validator as v


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=True, default='')

    @classmethod
    def find_by_id(cls, user_id: int) -> Any:  # here we use Any because it returns Any type
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def validate(cls, user, _id: int = 0):
        rules = {
            'username': v.stringType().length(min_value=3, max_value=64).alnum().noWhitespace().notExists(
                model=UserModel, column="username", obj_id=_id),
            'email': v.Optional(v.email())
        }

        return cls.fv().validate(user, rules)

    def get(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

    def update(self, data: Dict[str, Any]) -> 'UserModel':
        self.username = data['username'] if 'username' in data.keys() else self.username
        self.email = data['email'] if 'email' in data.keys() else self.email
        return self

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
