"""empty message

Revision ID: cd1cee7e744b
Revises: b7f4259fb042
Create Date: 2023-10-30 05:03:59.856145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd1cee7e744b'
down_revision = 'b7f4259fb042'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('programs', sa.Column('firstchoice', sa.String(), nullable=True))
    op.add_column('programs', sa.Column('seconschoice', sa.String(), nullable=True))
    op.add_column('programs', sa.Column('thirdchoice', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('programs', 'thirdchoice')
    op.drop_column('programs', 'seconschoice')
    op.drop_column('programs', 'firstchoice')
    # ### end Alembic commands ###
