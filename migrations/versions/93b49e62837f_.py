"""empty message

Revision ID: 93b49e62837f
Revises: 96b0e1efd34a
Create Date: 2023-11-01 16:37:42.785012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93b49e62837f'
down_revision = '96b0e1efd34a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applicantEmployment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.String(), nullable=False),
    sa.Column('usercode', sa.String(), nullable=False),
    sa.Column('institution', sa.String(), nullable=True),
    sa.Column('position', sa.String(), nullable=True),
    sa.Column('startdate', sa.DateTime(), nullable=True),
    sa.Column('enddate', sa.DateTime(), nullable=True),
    sa.Column('filed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('applicantEmployment')
    # ### end Alembic commands ###