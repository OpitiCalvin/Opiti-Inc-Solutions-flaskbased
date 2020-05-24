from flask import Blueprint

site = Blueprint('site', __name__, template_folder='../templates')

from . import home_views