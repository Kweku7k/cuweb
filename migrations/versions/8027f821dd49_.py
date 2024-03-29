"""empty message

Revision ID: 8027f821dd49
Revises: 15890fbf6742
Create Date: 2023-01-22 13:40:26.193749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8027f821dd49'
down_revision = '15890fbf6742'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('guardian',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.String(), nullable=False),
    sa.Column('usercode', sa.String(), nullable=False),
    sa.Column('relationship', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('mobile', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('occupation', sa.String(), nullable=True),
    sa.Column('filed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('guardian')
    # ### end Alembic commands ###
