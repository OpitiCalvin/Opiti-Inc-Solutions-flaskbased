from the_app import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from marshmallow import fields, Schema

from werkzeug.security import generate_password_hash, check_password_hash
from .user_roles import RoleModel, RoleInfoSchema

class UserModel(db.Model):
    r"""A db model to manage API users."""

    __tablename__ = 'api_user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey('user_role.role_id'), nullable=False)
    role = relationship('RoleModel', backref=db.backref('user_role', lazy=True))

    # flask login requirements
    authenticated = Column(Boolean, nullable=False, default=False, server_default="false")
    token = Column(String(500), nullable=True)

    # login tracker fields
    last_log_in = Column(DateTime(timezone=True), nullable=True)
    current_logged_in = Column(DateTime(timezone=True), nullable=True)

     # audit tracking fields
    created = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(30), nullable=False)
    updated = Column(DateTime(timezone=True),onupdate=func.now())
    updated_by = Column(String(30), nullable = True)

    def __repr__(self):
        return self.email

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def generate_hash(password):
        r"""
        A function to generate a hash equivalent of a user password.

        parameters
            password: str, required
                A text-based (unhashed) password

        returns
            A hashed or encrypted password.

        """

        return generate_password_hash(password, method="sha256")

    @staticmethod
    def verify_hash(hash, password):
        r"""
        A function to very text password match with hashed equivalent.

        parameters
            hash: str, required
                An encrypted or hashed password.

            password: str, required
                A text-based password.

        returns
            A boolean response on whether the passwords match.

        """

        return check_password_hash(hash, password)

    @property
    def is_active(self):
        return True

    def get_id(self):
        return self.user_id

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_anonymous(self):
        return False
    
class UserSchema(Schema):
    email = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    role_id  =fields.Integer(required=False)

class UserQuerySchema(Schema):
    user_id = fields.String()
    username = fields.String()
    email = fields.String()
    role_id = fields.Integer()
    role = fields.Nested(RoleInfoSchema)

    last_log_in = fields.Date()
    created_by = fields.String()
    created = fields.Date()
    updated_by = fields.String()
    update = fields.Date()
