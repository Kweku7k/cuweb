"""empty message

Revision ID: 15890fbf6742
Revises: b5333dce4a59
Create Date: 2023-01-22 13:12:27.319914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15890fbf6742'
down_revision = 'b5333dce4a59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('programs', schema=None) as batch_op:
        batch_op.drop_column('choice')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('programs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('choice', sa.DATETIME(), nullable=False))

    # ### end Alembic commands ###
