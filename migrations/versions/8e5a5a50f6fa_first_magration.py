"""First magration

Revision ID: 8e5a5a50f6fa
Revises: 
Create Date: 2023-07-05 14:59:06.828673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e5a5a50f6fa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('employee_number', sa.Integer(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('middle_name', sa.String(), nullable=True),
    sa.Column('birth_date', sa.DateTime(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('position', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('here_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employees_history',
    sa.Column('history_id', sa.Integer(), nullable=False),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('position', sa.String(), nullable=True),
    sa.Column('change_time', sa.DateTime(), nullable=True),
    sa.Column('change_type', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
    sa.PrimaryKeyConstraint('history_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employees_history')
    op.drop_table('employees')
    # ### end Alembic commands ###