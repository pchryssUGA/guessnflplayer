"""Initial migration

Revision ID: 017d48994cc3
Revises: 
Create Date: 2023-07-10 22:55:37.609698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '017d48994cc3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('team', sa.String(length=100), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.Column('numG', sa.Integer(), nullable=True),
    sa.Column('numC', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('team', sa.String(length=100), nullable=True),
    sa.Column('year', sa.String(length=100), nullable=True),
    sa.Column('numR', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reports')
    op.drop_table('players')
    # ### end Alembic commands ###
