"""create article_images table

Revision ID: 79db7f8947bd
Revises: 72f4f49a537e
Create Date: 2023-08-26 20:51:41.264662

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79db7f8947bd'
down_revision: Union[str, None] = '72f4f49a537e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'article_images',
        sa.Column('id', sa.String(36), primary_key=True, server_default=str(uuid.uuid4())),
        sa.Column('article_id', sa.String(36), nullable=False),
        sa.Column('image_url', sa.String(512), nullable=True),
        sa.Column('position', sa.Integer, nullable=False, server_default=0),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.NOW(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.NOW(), onupdate=sa.func.NOW(), nullable=False),
    )
    op.create_foreign_key("fk_article_images_article_id", 'article_images', 'articles',
                          ["article_id"], ["id"], ondelete='CASCADE', onupdate='CASCADE')

def downgrade() -> None:
    op.drop_table('article_images')

