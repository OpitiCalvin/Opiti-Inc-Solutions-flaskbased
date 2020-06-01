from flask import Blueprint
from flask_restx import Api

from .contact.resources import ns_messages

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="OPITI INC APIs.",
    version="1.0.0",
    # description="This api captures and manages messages from my website contact form."
    description = "APIs developed and managed by OPITI INC."
)

api.add_namespace(ns_messages)