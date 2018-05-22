"""user settings moodel added

Revision ID: 0d40e63af044
Revises: 4e7f3ec07ba5
Create Date: 2018-05-22 09:07:59.269627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d40e63af044'
down_revision = '4e7f3ec07ba5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('default_sys_username', sa.String(length=64), nullable=True),
    sa.Column('force_proxy', sa.Boolean(), nullable=True),
    sa.Column('proxy_host', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['proxy_host'], ['host.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_settings')
    # ### end Alembic commands ###
