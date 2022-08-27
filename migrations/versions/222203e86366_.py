"""empty message

Revision ID: 222203e86366
Revises: a82d3cf2bf52
Create Date: 2021-11-02 15:05:51.369661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '222203e86366'
down_revision = 'a82d3cf2bf52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('counter', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('created_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('last_checked', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_checked')
    op.drop_column('users', 'created_date')
    op.drop_column('users', 'counter')
    # ### end Alembic commands ###
