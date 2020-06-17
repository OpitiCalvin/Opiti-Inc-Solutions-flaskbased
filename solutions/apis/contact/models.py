from the_app import db
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from marshmallow import Schema, fields

class MessageModel(db.Model):
    r"""
    A db model for managing messages and contacts.

    """

    __tablename__ = 'message'

    message_id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(50), nullable = False)
    email = Column(String(50), nullable = False)
    phone = Column(String(15), nullable = True)
    country = Column(String(50), nullable = True)
    country_code = Column(String(3), nullable = True)
    subject = Column(String(20), nullable = False)
    message = Column(String(250), nullable = False)
    is_read = Column(Boolean, default=False)

    # audit tracking
    created = Column(DateTime(timezone = True), server_default = func.now())

    def __repr__(self):
        return f"{self.message_id}: name: {self.name}, subject: {self.subject}"

    # def __init__(self, name, email, subject, message):
    #     self.name = name
    #     self.email = email
    #     self.subject = subject
    #     self.message = message

    @classmethod
    def find_by_name(cls, name):
        r"""Queries for all messages using sender name."""

        return cls.query.filter_by(name = name).all()

    @classmethod
    def find_by_email(cls, email):
        r"""Queries for all messages using sender email."""
        
        return cls.query.filter_by(email = email).all()

class MessageSchema(Schema):
    r"""A schema for creation of messages."""

    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=False)
    country = fields.String(required=False)
    country_code = fields.String(required=False)
    subject = fields.String(required=True)
    message = fields.String(required = True)

class MessageQuerySchema(Schema):
    r"""A schema for querying of messages"""

    message_id = fields.Integer()
    name = fields.String()
    email = fields.String()
    phone = fields.String()
    country = fields.String()
    country_code = fields.String()
    subject = fields.String()
    message = fields.String()
    created = fields.Date()
    is_read = fields.Boolean()
