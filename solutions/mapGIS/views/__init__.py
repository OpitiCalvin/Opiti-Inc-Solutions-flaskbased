from flask import Blueprint

mapper = Blueprint('mapper', __name__, template_folder='../templates')

from . import mapper_views