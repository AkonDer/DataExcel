"""Corrected table EmployeeHistory

Revision ID: 7557fd8c1f95
Revises: e6b52438a95a
Create Date: 2023-07-26 16:40:17.034343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7557fd8c1f95'
down_revision = 'e6b52438a95a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('employees_history', 'old_position')
    op.drop_column('employees_history', 'old_address')
    op.drop_column('employees_history', 'old_last_name')
    op.drop_column('employees_history', 'old_status')
    op.drop_column('employees_history', 'old_department')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees_history', sa.Column('old_department', sa.VARCHAR(), nullable=True))
    op.add_column('employees_history', sa.Column('old_status', sa.VARCHAR(), nullable=True))
    op.add_column('employees_history', sa.Column('old_last_name', sa.VARCHAR(), nullable=True))
    op.add_column('employees_history', sa.Column('old_address', sa.VARCHAR(), nullable=True))
    op.add_column('employees_history', sa.Column('old_position', sa.VARCHAR(), nullable=True))
    # ### end Alembic commands ###