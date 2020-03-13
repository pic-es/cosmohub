from flask_sqlalchemy import SQLAlchemy
from marshmallow import validate
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import MetaData

from .naming import naming_convention


db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))


class BaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        # sqla_session = db.session
        include_relationships = False
        load_instance = True
        transient = True


class User(db.Model):
    """\
    User identities and profiles
    """

    __tablename__ = "user"
    __table_args__ = (
        # Primary key
        db.PrimaryKeyConstraint("id"),
        # Unique key
        db.UniqueConstraint("email"),
    )

    # Columns
    id = db.Column("id", db.Integer, nullable=False, comment="User unique identifier")
    name = db.Column("name", db.String(64), nullable=False, comment="Full name (for communications)")
    email = db.Column("email", db.String(254), nullable=False, comment="E-Mail address")

    def __repr__(self):
        return "%s(id=%s, name=%s, email=%s)" % (
            self.__class__.__name__,
            repr(self.id),
            repr(self.name),
            repr(self.email),
        )


class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = User
        dump_only = ["id"]

    email = auto_field(validate=validate.Email(error="Not a valid email address"))
