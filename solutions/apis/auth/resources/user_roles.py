from the_app import db
from flask import request, jsonify
from flask_restx import Resource, Namespace, fields, abort
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from marshmallow import ValidationError, validates

from . import ns_auth

from apis.auth.models.user_roles import RoleModel, RoleSchema, RoleQuerySchema, RoleUpdateSchema

role_schema = RoleSchema()
role_update_schema = RoleUpdateSchema()
roles_query_schema = RoleQuerySchema(many=True)
role_query_schema = RoleQuerySchema()

role_model = ns_auth.model("Role Model",{
    "role_id": fields.Integer(required=True, description="Unique identifier for the new role.",help="Role ID cannot be blank."),
    "name": fields.String(required=True, description="A unique role name.", help="Role name cannot be blank."),
    "description": fields.String(required=True, description="A short description of the new role.", help="Role description is required.")
})
role_update_model = ns_auth.model("Role Update Model",{
    "name": fields.String(required=True, description="A unique role name.", help="Role name cannot be blank."),
    "description": fields.String(required=True, description="A short description of the role.", help="Role description is required.")
})

@ns_auth.route("/roles")
class UserRoles(Resource):
    ns_auth.doc(
        responses = {
            200: "Success", 401: "Access Denied: Unauthorized Access",404: "Not Found",
            400: "Bad Request", 500: "Internal Server Error"
        }
    )

    def get(self):
        r"""Retrieves list of user roles."""

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        roles = RoleModel.query.all()
        if not roles:
            return abort(
                404,
                message="No user roles found."
            )

        json_response['code'] = 200
        json_response['message'] = "Query for user roles list successful."
        json_response['data'] = roles_query_schema.dump(roles)

        return jsonify(json_response)
    
    @ns_auth.expect(role_model)
    @jwt_required
    def post(self):
        r"""Creates a new role record."""

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        auth_token_info = get_jwt_identity()
        if auth_token_info['role'] == 1:
            try:
                data = request.get_json(force=True)
                if not data:
                    return abort(
                        400,
                        "No data provided."
                    )
                data_errors = role_schema.validate(data)
                if data_errors:
                    return abort(
                        400,
                        f"Schema validation errors: {data_errors}"
                    )
                roles = RoleModel.query.all()
                role_names = [role.name for role in roles]
                role_ids = [role.role_id for role in roles]
                if int(data['role_id']) in role_ids:
                    return abort(
                        400,
                        f"The provide role id already exists in the database. Please use an id other than these: {role_ids}"
                    )
                if data['name'] in role_names:
                    return abort(
                        400,
                        f"The role name provided is already in use. Please try a different and unique role name."
                    )
                new_role = RoleModel(
                    role_id = data['role_id'],
                    name = data['name'],
                    description = data['description'],
                    created_by = auth_token_info['username']
                )
                db.session.add(new_role)
                db.session.commit()

                json_response['code'] = 200
                json_response['message'] = "New user role successfully created."

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
                "Access Denied: Unauthorized Access"
            )

@ns_auth.route("/roles/<int:role_id>")
class SingleUserRole(Resource):
    r"""API resounce for query and manipulation of a single role record."""

    def get(self, role_id):
        r"""Retrieves an role record using its unique identifier.

        parameters
            role_id: int, required
                A unique identifier for the role record.

        returns
            A JSON response with the queried role record.

        """

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        role = RoleModel.find_by_role_id(role_id)
        if not role:
            return abort(
                404,
                f"No role record found with the role id {role_id}"
            )
        json_response['code'] = 200,
        json_response['message'] = "Query for user role successful."
        json_response['data'] = [role_query_schema.dump(role)]
        return jsonify(json_response)

    @ns_auth.expect(role_update_model)
    @jwt_required
    def put(self,role_id):
        r"""Update a user role record.

        parameters
            role_id: int, required
                A unique identifier for the role record.

        returns
            A JSON response with the status and message.

        """

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        auth_token_info = get_jwt_identity()
        if auth_token_info['role'] == 1:
            try:
                data = request.get_json(force=True)
                if not data:
                    return abort(
                        400,
                        "No data provided."
                    )
                data_errors = role_update_schema.validate(data)
                if data_errors:
                    return abort(
                        400,
                        f"Schema validation errors: {data_errors}"
                    )
                role = RoleModel.find_by_role_id(role_id)
                if not role:
                    return abort(
                        404,
                        f"No role record found with id {role_id}. Update request cancelled."
                    )
                role.name = data['name']
                role.description = data['description']

                db.session.commit()

                json_response['code'] = 200
                json_response['message'] = "Role record successfully updated."

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
                "Access Denied: Unauthorized Access"
            )

    @jwt_required
    def delete(self,role_id):
        r"""Deletes a user role record.

        parameters
            role_id: int, required
                A unique identifier for the role record.

        returns
            A JSON response with the status and message.

        """

        json_response = {
            "code": 400,
            "message": None,
            "errors": None,
            "data":[]
        }

        auth_token_info = get_jwt_identity()
        if auth_token_info['role'] == 1:
            try:
                role = RoleModel.find_by_role_id(role_id)
                if not role:
                    return abort(
                        404,
                        f"No role record found with id {role_id}. Delete request cancelled."
                    )
                db.session.delete(role)
                db.session.commit()

                json_response['code'] = 200
                json_response['message'] = "Role record successfully deleted."

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
                "Access Denied: Unauthorized Access"
            )