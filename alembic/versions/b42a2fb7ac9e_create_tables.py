"""create tables

Revision ID: b42a2fb7ac9e
Revises: 203a55dde622
Create Date: 2024-08-29 10:41:08.406168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'b42a2fb7ac9e'
down_revision: Union[str, None] = '203a55dde622'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_table('subcategories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subcategories_id'), 'subcategories', ['id'], unique=False)
    op.create_table('promotions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('discount_percentage', sa.Float(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_promotions_id'), 'promotions', ['id'], unique=False)
    op.create_table('reservations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('reserved_quantity', sa.Integer(), nullable=False),
    sa.Column('reservation_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reservations_id'), 'reservations', ['id'], unique=False)
    op.create_table('sales',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('sold_quantity', sa.Integer(), nullable=False),
    sa.Column('sale_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sales_id'), 'sales', ['id'], unique=False)
    op.add_column('products', sa.Column('stock', sa.Integer(), nullable=False))
    op.add_column('products', sa.Column('reserved_stock', sa.Integer(), nullable=True))
    op.add_column('products', sa.Column('subcategory_id', sa.Integer(), nullable=False))
    op.alter_column('products', 'name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('products', 'price',
               existing_type=mysql.INTEGER(),
               type_=sa.Float(),
               nullable=False)
    op.drop_index('ix_products_name', table_name='products')
    op.create_foreign_key(None, 'products', 'subcategories', ['subcategory_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.create_index('ix_products_name', 'products', ['name'], unique=False)
    op.alter_column('products', 'price',
               existing_type=sa.Float(),
               type_=mysql.INTEGER(),
               nullable=True)
    op.alter_column('products', 'name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.drop_column('products', 'subcategory_id')
    op.drop_column('products', 'reserved_stock')
    op.drop_column('products', 'stock')
    op.drop_index(op.f('ix_sales_id'), table_name='sales')
    op.drop_table('sales')
    op.drop_index(op.f('ix_reservations_id'), table_name='reservations')
    op.drop_table('reservations')
    op.drop_index(op.f('ix_promotions_id'), table_name='promotions')
    op.drop_table('promotions')
    op.drop_index(op.f('ix_subcategories_id'), table_name='subcategories')
    op.drop_table('subcategories')
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    op.drop_table('categories')
    # ### end Alembic commands ###
