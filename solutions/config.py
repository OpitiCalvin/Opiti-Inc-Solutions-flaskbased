import os
import json
import uuid
from ast import literal_eval

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	"""Parent configuration class."""

	if "FLASK_ENV" in os.environ:
		FLASK_ENV = os.environ.get("FLASK_ENV")
	else:
		FLASK_ENV = 'development'
	
	if FLASK_ENV == 'development':
		DEBUG = True
		# SECRET_KEY = "0e32f26c-5860-4da9-84bd-ca439074ba2a"
		SECRET_KEY = os.getenv("SECRET_KEY")
		# if 'POSTGRES' in os.environ:
		# 	POSTGRES = json.loads(os.environ.get('POSTGRES'))
		# elif "PGUSER" in os.environ and "PGPW" in os.environ and "PGHOST" in os.environ and "PGPORT" in os.environ and "PGDB" in os.environ:
		# 	POSTGRES = dict(user=os.environ.get("PGUSER"),pw=os.environ.get("PGPW"),host=os.environ.get("PGHOST"),port=os.environ.get("PGPORT"),db=os.environ.get("PGDB"))
		# else:
		# 	print("Postgresql configuration parameters not found.")	
		# 	exit(1)
		
		SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'opiti_inc_solutions.sqlite')
		# SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
		
	else:
		TESTING = False
		SECRET_KEY = uuid.uuid4().hex
		# SECRET_KEY = os.getenv("SECRET_KEY")
		if 'POSTGRES' in os.environ:
			POSTGRES = json.loads(os.environ.get('POSTGRES'))
		elif "PGUSER" in os.environ and "PGPW" in os.environ and "PGHOST" in os.environ and "PGPORT" in os.environ and "PGDB" in os.environ:
			POSTGRES = dict(user=os.environ.get("PGUSER"),pw=os.environ.get("PGPW"),host=os.environ.get("PGHOST"),port=os.environ.get("PGPORT"),db=os.environ.get("PGDB"))
		else:
			print("Postgresql configuration parameters not found.")	
			exit(1)
		
		SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
		CUSTOM_DB_FLAG = 'production'
		DEBUG = False
		
		JSON_SORT_KEYS = False

	SQLALCHEMY_TRACK_MODIFICATIONS = False
	PROPAGAGE_EXCEPTIONS = True