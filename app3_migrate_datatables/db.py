from datetime import datetime

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import MetaData
from respect_validation import FormValidator


convention = {
    "ix": "ix_%(column_0_lable)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


class TimestampsModel(Model):
    created_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP, server_default=sqlalchemy.func.now())
    updated_at = sqlalchemy.Column(
                sqlalchemy.TIMESTAMP, server_default=sqlalchemy.func.now())


class ValidationModel(Model):

    @staticmethod
    def _output_serialization(data, date_format: str = "%Y-%m-%d %H:%M:%S"):
        if isinstance(data, str) or isinstance(data, int) or data is None:
            return data
        if isinstance(data, datetime):
            return data.strftime(date_format)
        return str(data)

    @staticmethod
    def fv() -> 'FormValidator':
        return FormValidator()

    def save(self) -> None:
        if hasattr(self, "updated_at"):
            self.updated_at = sqlalchemy.func.now()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata, model_class=ValidationModel)
