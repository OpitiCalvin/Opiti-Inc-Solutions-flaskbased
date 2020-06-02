from flask import Blueprint
from flask_restx import Api
from flask_cors import CORS

from .contact.resources import ns_messages

blueprint = Blueprint("api", __name__)
CORS(blueprint) # enable CORS on the api blueprint

api = Api(
    blueprint,
    title="OPITI INC APIs.",
    version="1.0.0",
    # description="This api captures and manages messages from my website contact form."
    description = "APIs developed and managed by OPITI INC."
)

api.add_namespace(ns_messages)
