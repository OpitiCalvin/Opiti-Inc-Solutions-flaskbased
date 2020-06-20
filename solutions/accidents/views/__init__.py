from flask import Blueprint

county = Blueprint('county', __name__, template_folder='../templates')

from . import accidents