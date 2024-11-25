"""Add agenda and expert_comment to tips

Revision ID: 15eb85886e92
Revises: bc3295460cb6
Create Date: 2024-11-25 23:05:22.034847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15eb85886e92'
down_revision = 'bc3295460cb6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tips', schema=None) as batch_op:
        batch_op.add_column(sa.Column('agenda', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('expert_comment', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('upvotes', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('downvotes', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tips', schema=None) as batch_op:
        batch_op.drop_column('downvotes')
        batch_op.drop_column('upvotes')
        batch_op.drop_column('expert_comment')
        batch_op.drop_column('agenda')

    # ### end Alembic commands ###
