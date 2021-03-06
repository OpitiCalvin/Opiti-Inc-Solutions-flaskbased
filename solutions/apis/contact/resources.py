from the_app import db
from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource, fields, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import MessageModel, MessageQuerySchema, MessageSchema

message_schema = MessageSchema()
messages_query_schema = MessageQuerySchema(many=True)
message_query_schema = MessageQuerySchema()

ns_messages = Namespace("Management of Contact Messages", description="Management of contacts and messages from my website.")

message_model = ns_messages.model(
    "Messages Model",
    {
        "name": fields.String(required=True, description="Person's names.", help="Name cannot be blank."),
        "email": fields.String(required=True, description="Person's contact email address.", help="Email cannot be blank."),
        "phone": fields.String(required=False, description="Person's contact phone numbers", help="Email can be blank."),
        "subject": fields.String(required=True, description="Message heading or topic", help="Subject cannot be blank."),
        "message": fields.String(required=True, description="Message content.", help="Message cannot be blank.")
    }
)

@ns_messages.route("")
class MessagesResource(Resource):
    ns_messages.doc(
        responses = {
            200: "Success", 404: "Not Found",
            400: "Bad Request", 500: "Internal Server Error"
        }
    )
    @jwt_required
    def get(self):
        r"""
        Retrieves all messages from the database.

        """

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        auth_token_info = get_jwt_identity()
        if auth_token_info['role'] == 1:
            messages = MessageModel.query.all()
            if not messages:
                return abort(
                        404,
                        message = "No messages found."
                    )
            json_response["code"] = 200
            json_response["message"] = "Query for messages successful."
            json_response["data"] = messages_query_schema.dump(messages)

            return jsonify(json_response)

        else:
            return abort(
                401,
                "Access Denied: Unauthorized Access."
            )
        
    ns_messages.doc(
        responses = {
            200: "Success", 404: "Not Found",
            400: "Bad Request", 500: "Internal Server Error"
        }
    )
    @ns_messages.expect(message_model)
    def post(self):
        r"""Creates a new message record."""

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        
        data = request.get_json(force=True)
        if not data:
            return abort(
                400,
                message = "Bad Request: No input data provided."
            )
        # print(data)
        validation_errors = message_schema.validate(data)
        if validation_errors:
            return abort(
                400,
                message = f"Bad Request: Schema validation Errors: {validation_errors}"
            )

        if "phone" in data.keys():
            phone = data["phone"]
        else:
            phone = None

        if "country" in data.keys():
            country = data["country"]
        else:
            country = None

        if "country_code" in data.keys():
            country_code = data["country_code"]
        else:
            country_code = None
            
        try:
            message = MessageModel(
                name = data["name"],
                email = data["email"],
                phone = phone,
                country = country,
                country_code = country_code,
                subject = data["subject"],
                message = data["message"]
            )

            db.session.add(message)
            db.session.commit()

            json_response["code"] = 200
            json_response["message"] = "Message successfully sent."

            return jsonify(json_response)
        except Exception as e:
            db.session.rollback()
            return abort(
                422,
                message= f"Unprocessable entiry occurred.{e.args}"
            )

@ns_messages.route("/<message_id>")
class MessageResource(Resource):
    @ns_messages.doc(
        responses = {
            200: "Success", 404: "Not Found",
            400: "Bad Request", 500: "Internal Server Error"
        },
        params={"message_id": "Unique identifier for the message record."}
    )
    @jwt_required
    def get(self, message_id):
        r"""
        Retrieves a single message record.

        parameters

            message_id: int, required
                A unique identifier for a message record.

        """

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        auth_token_info = get_jwt_identity()
        if auth_token_info['role'] == 1:
            message = MessageModel.query.filter_by(message_id = message_id).first()
            if not message:
                return abort(
                    404,
                    message= "Not Found: Message record not found.",
                    errors= None,
                    data = []
                )

            json_response["code"] = 200
            json_response["message"] = "Query for message record successful."
            json_response["data"] = [message_query_schema.dump(message)]

            return jsonify(json_response)
        else:
            return abort(
                401,
                "Access Denied: Unauthorized Access."
            )

    @ns_messages.doc(
        responses = {
            200: "Success", 404: "Not Found",
            400: "Bad Request", 500: "Internal Server Error"
        },
        params={"message_id": "Unique identifier for the message record."}
    )
    @jwt_required
    def delete(self, message_id):
        r"""
        Deletes a single message record.

        parameters

            message_id: int, required
                A unique identifier for a message record.

        """

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        auth_token_info = get_jwt_identity()
        if auth_token_info['role'] == 1:
            msg = MessageModel.query.filter_by(message_id = message_id).first()
            if not msg:
                return abort(
                    404,
                    f"Not Found: No message record found with id {message_id}"
                )
            db.session.delete(msg)
            db.session.commit()

            json_response['code'] = 200
            json_response['message'] = "Message record successfully deleted."

            return jsonify(json_response)
        else:
            return abort(
                401,
                "Access Denied: Unauthorized Access."
            )
