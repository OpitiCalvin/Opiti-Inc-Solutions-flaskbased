from flask import Blueprint
from flask_restx import Api

msg_bp = Blueprint("msg_api", __name__)

msg_api = Api(
    msg_bp,
    title="Api for management for website messages and contacts.",
    version="1.0.0",
    description="This api captures and manages messages from my website contact form."
)

from . import views