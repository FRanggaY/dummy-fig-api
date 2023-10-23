"""create article_categories table

Revision ID: afd8e32af55e
Revises: 627966fd935e
Create Date: 2023-10-23 22:35:15.152042

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afd8e32af55e'
down_revision: Union[str, None] = '627966fd935e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'article_categories',
        sa.Column('id', sa.String(36), primary_key=True, server_default=str(uuid.uuid4())),
        sa.Column('article_id', sa.String(36), nullable=False),
        sa.Column('category_id', sa.String(36), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.NOW(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.NOW(), onupdate=sa.func.NOW(), nullable=False),
    )
    op.create_foreign_key("fk_article_categories_article_id", 'article_categories', 'articles',
                          ["article_id"], ["id"], ondelete='CASCADE', onupdate='CASCADE')
    op.create_foreign_key("fk_article_categories_category_id", 'article_categories', 'categories',
                          ["category_id"], ["id"], ondelete='CASCADE', onupdate='CASCADE')

def downgrade() -> None:
    op.drop_table('article_categories')
