"""create user table

Revision ID: 57de49e139ad
Revises: 
Create Date: 2023-08-17 19:31:01.224056

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57de49e139ad'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True, server_default=str(uuid.uuid4())),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('email', sa.String(50), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(512), nullable=False),
        sa.Column('status', sa.Enum('active', 'inactive', 'idle'), server_default='inactive', nullable=False),
        sa.Column('email_verified_at', sa.DateTime, nullable=True),
        sa.Column('last_login_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.NOW(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.NOW(), onupdate=sa.func.NOW(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('users')
