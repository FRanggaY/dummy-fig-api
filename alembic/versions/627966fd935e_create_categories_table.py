"""create categories table

Revision ID: 627966fd935e
Revises: 79db7f8947bd
Create Date: 2023-10-23 22:33:39.649293

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '627966fd935e'
down_revision: Union[str, None] = '79db7f8947bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'categories',
        sa.Column('id', sa.String(36), primary_key=True, server_default=str(uuid.uuid4())),
        sa.Column('label', sa.String(50), unique=True, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.NOW(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.NOW(), onupdate=sa.func.NOW(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('categories')
