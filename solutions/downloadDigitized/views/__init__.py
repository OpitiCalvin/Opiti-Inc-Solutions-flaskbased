from flask import Blueprint

dnd = Blueprint('dnd_app', __name__, template_folder='../templates')

from . import dnd_views