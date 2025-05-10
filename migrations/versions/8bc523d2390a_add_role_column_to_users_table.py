"""Add role column to users table

Revision ID: 8bc523d2390a
Revises: db1eafbc3125
Create Date: 2025-05-08 12:06:09.660365
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8bc523d2390a'
down_revision = 'db1eafbc3125'
branch_labels = None
depends_on = None

def upgrade():
    # Add 'role' column to 'users' table with default value 'user'
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('role', sa.String(length=50), nullable=False, server_default='user')
        )

def downgrade():
    # Remove 'role' column from 'users' table
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('role')
