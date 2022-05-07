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


class ValidationModel(Model):

    @classmethod
    def fv(cls) -> 'FormValidator':
        return FormValidator()


metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata, model_class=ValidationModel)
