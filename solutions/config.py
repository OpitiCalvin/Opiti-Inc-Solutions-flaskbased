import os
import json
import uuid
from ast import literal_eval

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	"""Parent configuration class."""

	DEBUG = False	
	

class DevelopmentConfig(Config):
	"""Configuration for development environment."""
	
	DEBUG = True
	SECRET_KEY = os.getenv("SECRET_KEY")
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'opiti_inc_solns.sqlite')
	# SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % literal_eval(os.getenv("POSTGRES")) # for postgresql
	
	CUSTOM_DB_FLAG = 'local'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	# UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'geofarmer_apis','uploads')
	# UPLOADED_IMAGES_DEST = os.path.join(basedir, 'geofarmer_apis','uploads', 'logo')
	# UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'geofarmer_apis','uploads', 'disp_pic')

class ProductionConfig(Config):
	"""
	Configurations for Production Environment.

	"""
	
	TESTING = False
	SECRET_KEY = uuid.uuid4().hex
	# SECRET_KEY = os.getenv("SECRET_KEY")
	# SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % literal_eval(os.getenv("POSTGRES")) # for postgresql
	CUSTOM_DB_FLAG = 'production'
	DEBUG = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	JSON_SORT_KEYS = False
	# UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'geofarmer_api','uploads')
	# UPLOADED_IMAGES_DEST = os.path.join(basedir, 'geofarmer_api','uploads', 'logo')
	# UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'geofarmer_api','uploads', 'disp_pic')

	
if os.getenv('APP_ENV') == 'development':
	app_config = DevelopmentConfig
else:
	app_config = ProductionConfig

# app_config = {
# 	'development': DevelopmentConfig,
# 	'production': ProductionConfig,
# }
