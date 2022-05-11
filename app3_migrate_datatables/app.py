from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from db import db
from routes import RouteMaker
from config import API_PORT, API_HOST, API_DEBUG, API_DATABASE

from respect_validation import Factory
Factory.add_rules_packages('src.validation.rules')
Factory.add_exceptions_packages('src.validation.exceptions')

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = API_DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# flask_restful
api = Api(app)
# flask_sqlalchemy
db.init_app(app)
# flask_migrate
migrate = Migrate(app, db)
migrate.init_app(app)

RouteMaker.run(api=api)

if __name__ == '__main__':
    app.run(port=API_PORT, host=API_HOST, debug=API_DEBUG)
