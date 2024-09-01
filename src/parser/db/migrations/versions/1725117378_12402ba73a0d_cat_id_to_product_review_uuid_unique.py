"""cat id to product, review uuid unique

Revision ID: 12402ba73a0d
Revises: 998055af4602
Create Date: 2024-08-31 18:16:18.407581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12402ba73a0d'
down_revision: Union[str, None] = '998055af4602'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mp_ozon_product', sa.Column('category_id', sa.Integer(), nullable=True, comment='FK to the category which triggered parsing of this product'))
    op.create_foreign_key('mp_ozon_product_category_id_fk', 'mp_ozon_product', 'mp_ozon_category', ['category_id'], ['id'])
    op.alter_column('mp_ozon_review', 'review_uuid',
               existing_type=sa.VARCHAR(length=36),
               nullable=False,
               existing_comment='Unique identifier for the review')
    op.create_unique_constraint('mp_ozon_review_review_uuid_uq', 'mp_ozon_review', ['review_uuid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('mp_ozon_review_review_uuid_uq', 'mp_ozon_review', type_='unique')
    op.alter_column('mp_ozon_review', 'review_uuid',
               existing_type=sa.VARCHAR(length=36),
               nullable=True,
               existing_comment='Unique identifier for the review')
    op.drop_constraint('mp_ozon_product_category_id_fk', 'mp_ozon_product', type_='foreignkey')
    op.drop_column('mp_ozon_product', 'category_id')
    # ### end Alembic commands ###
