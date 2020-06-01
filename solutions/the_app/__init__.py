from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from pathlib import Path

db = SQLAlchemy()
# ma = Marshmallow()
migrate = Migrate()

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

def register_blueprints(app):
	r"""

	"""

	# API section
	
	from apis import blueprint
	app.register_blueprint(blueprint, url_prefix="/api")

	# Solutions section
	
	from home.views import site as home_bp
	app.register_blueprint(home_bp, url_prefix="")

	from downloadDigitized.views import dnd as dnd_bp
	app.register_blueprint(dnd_bp, url_prefix="/Download-Digitized")

	from mapGIS.views import mapper as mapper_bp
	app.register_blueprint(mapper_bp, url_prefix="/mapGIS")

