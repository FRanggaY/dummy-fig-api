"""create article table

Revision ID: 72f4f49a537e
Revises: 57de49e139ad
Create Date: 2023-08-19 19:32:23.645360

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72f4f49a537e'
down_revision: Union[str, None] = '57de49e139ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'articles',
        sa.Column('id', sa.String(36), primary_key=True, server_default=str(uuid.uuid4())),
        sa.Column('title', sa.String(50), unique=True, nullable=False),
        sa.Column('slug', sa.String(60), unique=True, nullable=False),
        sa.Column('headline', sa.String(1024), nullable=True),
        sa.Column('description', sa.String(2048), nullable=True),
        sa.Column('image_url', sa.String(512), nullable=True),
        sa.Column('author', sa.String(128), nullable=True),
        sa.Column('status', sa.Enum('draft', 'flagged', 'archived', 'publish'), server_default='draft', nullable=False),
        sa.Column('lang', sa.Enum('en', 'id'), server_default='id', nullable=False),
        sa.Column('published_at', sa.Date, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.NOW(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.NOW(), onupdate=sa.func.NOW(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('articles')
