"""empty message

Revision ID: b37aed99021f
Revises: 6adf79447673
Create Date: 2023-01-22 13:10:25.315448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b37aed99021f'
down_revision = '6adf79447673'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('programs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.String(), nullable=False),
    sa.Column('usercode', sa.String(), nullable=False),
    sa.Column('program', sa.String(), nullable=False),
    sa.Column('choice', sa.DateTime(), nullable=False),
    sa.Column('entry_mode', sa.String(), nullable=True),
    sa.Column('filed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('programs')
    # ### end Alembic commands ###
