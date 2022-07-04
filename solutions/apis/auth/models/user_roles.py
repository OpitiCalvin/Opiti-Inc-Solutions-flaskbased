from the_app import db
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.sql import func
from marshmallow import fields, Schema

class RoleModel(db.Model):
    r"""A db model for management of user role records."""

    __tablename__ = "user_role"

    role_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20), nullable=False, unique=True)
    description = Column(String(200), nullable=False)

    # audit tracking fields
    created = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(30), nullable=False)
    updated = Column(DateTime(timezone=True),onupdate=func.now())
    updated_by = Column(String(30), nullable = True)

    def __repr__(self):
        return self.name

    @classmethod
    def find_by_role_name(cls, name):
        return cls.query.filter_by(name = name).first()

    @classmethod
    def find_by_role_id(cls, role_id):
        return cls.query.filter_by(role_id=role_id).first()

class RoleSchema(Schema):
    role_id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)

class RoleUpdateSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)

class RoleQuerySchema(Schema):
    role_id = fields.Integer()
    name = fields.String()
    description = fields.String()
    created_by = fields.String()
    created = fields.Date()
    updated_by = fields.String()
    update = fields.Date()

class RoleInfoSchema(Schema):
    name = fields.String()
