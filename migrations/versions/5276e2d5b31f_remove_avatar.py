"""remove avatar

Revision ID: 5276e2d5b31f
Revises: a55109e92538
Create Date: 2021-07-15 00:17:26.139510

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5276e2d5b31f'
down_revision = 'a55109e92538'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_avatar', table_name='user')
    op.drop_column('user', 'avatar')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar', mysql.VARCHAR(length=64), nullable=True))
    op.create_index('ix_user_avatar', 'user', ['avatar'], unique=False)
    # ### end Alembic commands ###