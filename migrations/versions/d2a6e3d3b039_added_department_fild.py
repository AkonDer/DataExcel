"""Added department fild

Revision ID: d2a6e3d3b039
Revises: 8e5a5a50f6fa
Create Date: 2023-07-05 15:13:56.174645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2a6e3d3b039'
down_revision = '8e5a5a50f6fa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees', sa.Column('department', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('employees', 'department')
    # ### end Alembic commands ###