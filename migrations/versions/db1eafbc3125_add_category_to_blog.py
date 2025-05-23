"""Add category to Blog

Revision ID: db1eafbc3125
Revises: 71b4c52ba1f4
Create Date: 2025-05-07 20:04:37.930431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db1eafbc3125'
down_revision = '71b4c52ba1f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blogs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blogs', schema=None) as batch_op:
        batch_op.drop_column('category')

    # ### end Alembic commands ###
