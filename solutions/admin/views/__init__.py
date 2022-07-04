from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder='../templates')

from . import user_management
from . import message_management