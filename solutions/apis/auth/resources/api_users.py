from the_app import db
from flask import request, jsonify
from flask_restx import Resource, fields, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt

from . import ns_auth
import datetime

from apis.auth.models.api_users import UserModel, UserQuerySchema, UserSchema
from apis.auth.models.tokens import RevokedTokenModel
from apis.auth.models.user_roles import RoleModel

user_schema = UserSchema()
users_query_schema = UserQuerySchema(many=True)
user_query_schema = UserQuerySchema()

user_model = ns_auth.model("User Model",{
    "username": fields.String(required=True, description="User's username", help="Username cannot be blank."),
    "password": fields.String(required=True, description="User's password", help="Password cannot be blank."),
    "email": fields.String(required=True, description="User's contact e-mail address.", help="Email canno be blank."),
    "role_id": fields.Integer(required=False, description="Role level assigned to the user.", help="If not provided, a default role level is assigned.")
})

@ns_auth.route("/login")
class UserAuth(Resource):
    @ns_auth.doc(
        responses = {
            200: "Success", 401: "Access Denied: Unauthorized Access",404: "Not Found",
            400: "Bad Request", 500: "Internal Server Error"
        }
    )
    def post(self):
        r"""Authenticate a user and generated a JWT token."""

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return abort(
                401,
                "Access Denied: Username and Password required to login."
            )
        user = UserModel.find_by_username(username=auth.username)
        if not user:
            user = UserModel.find_by_email(email = auth.username)
            if not user:
                return abort(
                    401,
                    "Access Denied: No user record found with provided username or email."
                )
            else:
                json_response['warnings'] = "Email was used as username."

        if UserModel.verify_hash(user.password, auth.password):
            token = create_access_token(
                identity={
                    "username": user.username,
                    "email": user.email,
                    "role": user.role_id,
                },
                expires_delta=datetime.timedelta(hours=5) # expires in 5 hours
            )
            json_response['code'] = 200
            json_response['message'] = "User authorization successful."
            json_response['data'] = [{"token": token}]
            return jsonify(json_response)
        else:
            return abort(
                401,
                "Acces Denied: Unauthorized Access."
            )

@ns_auth.route("/logout")
class UserLogout(Resource):
    
    @ns_auth.doc(
        responses = {
            200: "Success", 401: "Access Denied: Unauthorized Access",404: "Not Found",
            400: "Bad Request", 500: "Internal Server Error"
        }
    )
    @jwt_required
    def post(self):
        r"""Logout a user and revoke JWT token."""

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        token = get_raw_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(token=token)
            db.session.add(revoked_token)
            db.session.commit()

            json_response['code'] = 200
            json_response['message'] = "User logged out and token revoked."
            return jsonify(json_response)
        except Exception as e:
            db.session.rollback()
            return abort(
                500,
                f"Internal Server Error during logout and token revoking. {e.args}"
            )

@ns_auth.route("/users")
class APIUsers(Resource):
    @ns_auth.doc(
        responses = {
            200: "Success", 401: "Access Denied: Unauthorized Access",404: "Not Found",
            400: "Bad Request", 500: "Internal Server Error"
        }
    )
    @jwt_required
    def get(self):
        r"""Retrieves list of all API users."""

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        auth_token_info = get_jwt_identity()
        if auth_token_info['role'] == 1:
            users = UserModel.query.all()
            if not users:
                return abort(
                    404,
                    "No user records found in the database."
                )
            json_response['code'] = 200
            json_response['message'] = "Query for users successful."
            json_response['data'] = users_query_schema.dump(users)

            return jsonify(json_response)
        else:
            user = UserModel.find_by_username(auth_token_info['username'])
            if not user:
                return abort(
                    404,
                    "No user records found in the database."
                )
            json_response['code'] = 200
            json_response['message'] = "Query for user successful."
            json_response['data'] = [user_query_schema.dump(user)]

            return jsonify(json_response)

    @ns_auth.doc(
        responses = {
            200: "Success", 401: "Access Denied: Unauthorized Access",404: "Not Found",
            400: "Bad Request", 500: "Internal Server Error"
        }
    )
    @ns_auth.expect(user_model)
    @jwt_required
    def post(self):
        r"""Create a new user record."""

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        auth_token_info = get_jwt_identity()
        if auth_token_info['role'] == 1:
            data = request.get_json(force=True)
            if not data:
                return abort(
                    400,
                    "Bad Request: No data provided."
                )
            data_errors = user_schema.validate(data)
            if data_errors:
                return abort(
                    400,
                    f"An error occurred: {data_errors}"
                )
            email_check = UserModel.find_by_email(data["email"])
            if email_check:
                return abort(
                    400,
                    f"Bad Request: The email {data['email']} is already in use. Please try another."
                )
            username_check = User.find_by_username(data["username"])
            if username_check:
                return abort(
                    400,
                    f"Bad Request: The username {username} is already in use. Please try another."
                )
            try:
                new_user  = UserModel(
                    username = data['username'],
                    password = UserModel.generate_hash(data['password']),
                    email = data['email'],
                    role_id = data['role_id'],
                    created_by = auth_token_info['username']
                )
                db.session.add(new_user)
                db.session.commit()

                json_response['code'] = 200
                json_response['message'] = "New user record successfully created."
                return jsonify(json_response)

            except Exception as e:
                db.session.rollback()
                return abort(
                    400,
                    f"An error occurred: {e.args}"
                )

        else:
            return abort(
                401,
                "Access Denied: Unauthorized Access."
            )

@ns_auth.route("/users/<int:user_id>")
class SingleUser(Resource):
    @ns_auth.doc(
        responses = {
            200: "Success", 401: "Access Denied: Unauthorized Access",404: "Not Found",
            400: "Bad Request", 500: "Internal Server Error"
        }
    )
    @jwt_required
    def get(self, user_id):
        r"""
        Retrieves a user record based on a user ID.

        parameters
            user_id: int, required
                A unique identifier for a user record.

        returns
            A JSON response with the queried user record.
        
        """

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        auth_token_info = get_jwt_identity()
        if auth_token_info['role'] == 1:
            user = UserModel.find_by_user_id(user_id)
            if not user:
                return abort(
                    404,
                    f"No user record found with ID {user_id}"
                )
            json_response['code'] = 200
            json_response['message'] = "Query for user successful."
            json_response['data'] = [user_query_schema.dump(user)]

            return jsonify(json_response)

        elif auth_token_info['role'] > 1:
            if user_id != auth_token_info['role']:
                return abort(
                    404,
                    f"No user record found with the ID {user_id}"
                )
            json_response['code'] = 200
            json_response['message'] = "Query for user successful."
            json_response['data'] = [user_query_schema.dump(user)]

            return jsonify(json_response)

        else:
            return abort(
                401,
                "Access Denied: Unauthorized Access."
            )
    
    @ns_auth.doc(
        responses = {
            200: "Success", 401: "Access Denied: Unauthorized Access",404: "Not Found",
            400: "Bad Request", 500: "Internal Server Error"
        }
    )
    @jwt_required
    def delete(self, user_id):
        r"""
        Deletes a user record based on a user ID.

        parameters
            user_id: int, required
                A unique identifier for a user record.

        returns
            A JSON response with the message and status of the delete task.
        
        """

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        auth_token_info = get_jwt_identity()
        if auth_token_info['role'] == 1:
            user = UserModel.find_by_user_id(user_id)
            if not user:
                return abort(
                    404,
                    f"Not Found: No user rocord with ID {user_id} found. Deletion task cancelled."
                )
            db.session.delete(user)
            db.session.commit()

            json_response['code'] = 200
            json_response['message'] = "User record successfully deleted."
            return jsonify(json_response)

        else:
            return abort(
                401,
                "Access Denied: Unauthorized Access."
            )