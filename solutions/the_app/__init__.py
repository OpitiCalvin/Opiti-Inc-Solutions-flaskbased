from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_login import LoginManager

from pathlib import Path

db = SQLAlchemy()
# ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()
login_manager = LoginManager()

def create_app():
	r"""
	Initializes the flask application.

	"""

	app = Flask(__name__, instance_relative_config=True, static_folder='../static')
	app.config.from_object("config.Config")

	if not Path(app.instance_path).exists():
		Path(app.instance_path).mkdir(parents=True, exist_ok=True)

	initialize_extension(app)
	register_blueprints(app)
	
	return app

def initialize_extension(app):
	r"""

	"""

	db.init_app(app)
	# ma.init_app(app)
	migrate.init_app(app)
	jwt.init_app(app)
	login_manager.init_app(app)

def register_blueprints(app):
	r"""

	"""

	# API section
	
	from apis import blueprint
	app.register_blueprint(blueprint, url_prefix="/api")

	# Solutions section
	from admin.views import admin as admin_bp
	app.register_blueprint(admin_bp, url_prefix="/admin")
	
	from home.views import site as home_bp
	app.register_blueprint(home_bp, url_prefix="")

	from downloadDigitized.views import dnd as dnd_bp
	app.register_blueprint(dnd_bp, url_prefix="/Download-Digitized")

	from mapGIS.views import mapper as mapper_bp
	app.register_blueprint(mapper_bp, url_prefix="/mapGIS")

	from accidents.views import county as county_bp
	app.register_blueprint(county_bp, url_prefix="/accidents")