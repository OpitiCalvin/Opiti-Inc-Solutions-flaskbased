from the_app import db, jwt
from flask import jsonify, abort

from apis.auth.models.api_users import UserModel
from apis.auth.models.tokens import RevokedTokenModel

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    r"""
    Validates a token for its revoked or validity status.

    parameters
        decrypted_token: JWToken, required
            A token to be checked if revoked or still valid.

    returns
        A boolean response on validity of the token
    
    """

    token = decrypted_token['jti']
    return RevokedTokenModel.is_token_blacklisted(token)

@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    r"""Validates a token to check if it has expired or not.

    parameters:
        expired_token: JWToken, required
            The token to be validated.

    returns
        A JSON response message if a token has expired.

    """

    token_type = expired_token["type"]
    return abort(
        401,
        f"The {token_type} token has expired. Please login to generate a new one."
    )

@jwt.revoked_token_loader
def revoked_token_callback():
    r"""A JWT loader function for tokens validated and marked as revoked."""

    return abort(
        401,
        "The token has been revoked"
    )