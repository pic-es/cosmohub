"""Initial user toy model.

Revision ID: 23cb7bdc76b8
Revises: 
Create Date: 2020-03-05 10:54:44.947417

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "23cb7bdc76b8"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False, comment="User unique identifier"),
        sa.Column("name", sa.String(length=64), nullable=False, comment="Full name (for communications)"),
        sa.Column("email", sa.String(length=254), nullable=False, comment="E-Mail address"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__user")),
        sa.UniqueConstraint("email", name=op.f("uq__user__email")),
    )


def downgrade():
    op.drop_table("user")
