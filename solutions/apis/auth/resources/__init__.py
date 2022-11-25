from flask_restx import Namespace

ns_auth = Namespace('User Authentication and Authorisation', description="Main authentication and authorization API resources.")

from apis.auth.functions import token_validation

from . import api_users
from . import user_roles