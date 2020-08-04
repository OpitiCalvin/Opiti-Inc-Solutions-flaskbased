from the_app import db
from sqlalchemy import Column, Integer, String

class RevokedTokenModel(db.Model):
    r"""A db model to capture revoked JWT tokens."""

    __tablename__ = "revoked_token"

    id = Column(Integer, primary_key=True)
    token = Column(String(120))

    def ad(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_token_blacklisted(cls, token):
        r"""
        Queries db to check if provided token has been revoked.

        parameter
            token: str, required
                The JWT token to be validated.

        returns
            A boolean response on validity of the token or not.

        """

        query = cls.query.filter_by(token = token).first()
        return bool(query)