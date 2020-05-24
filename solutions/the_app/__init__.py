from flask import Flask

from pathlib import Path

def create_app():
	r"""
	Initializes the flask application.

	"""

	app = Flask(__name__, instance_relative_config=True, static_folder='../static')
	app.config.from_object("config.app_config")

	if not Path(app.instance_path).exists():
		Path(app.instance_path).mkdir(parents=True, exist_ok=True)

	initialize_extension(app)
	register_blueprints(app)
	
	return app

def initialize_extension(app):
	r"""

	"""

	pass

def register_blueprints(app):
	r"""

	"""

	from home.views import site as home_bp
	app.register_blueprint(home_bp, url_prefix="")

	from downloadDigitized.views import dnd as dnd_bp
	app.register_blueprint(dnd_bp, url_prefix="/Download-Digitized")

	from mapGIS.views import mapper as mapper_bp
	app.register_blueprint(mapper_bp, url_prefix="/mapGIS")

