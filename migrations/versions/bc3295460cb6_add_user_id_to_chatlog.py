"""Add user_id to ChatLog

Revision ID: bc3295460cb6
Revises: 38ecb5d34dc1
Create Date: 2024-11-25 11:25:46.866230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc3295460cb6'
down_revision = '38ecb5d34dc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_log', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
          # 外部キー制約を追加
        batch_op.create_foreign_key(
            constraint_name="fk_chat_log_user_id",  # 制約名を指定
            referent_table="users",
            local_cols=["user_id"],
            remote_cols=["id"]
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_log', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    op.create_table('counselor_chat',
    sa.Column('room_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('counselor_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['counselor_id'], ['counselor_chat_message.id'], ),
    sa.ForeignKeyConstraint(['room_id'], ['counselor_chat_room.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('room_id', 'user_id', 'counselor_id')
    )
    op.create_table('counselor_chat_message',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('room_id', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('message', sa.TEXT(), nullable=False),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['counselor_chat_room.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('tag', sa.VARCHAR(length=50), nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), nullable=False),
    sa.Column('link', sa.VARCHAR(length=200), nullable=False),
    sa.Column('publish_comment', sa.TEXT(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vote',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('article_id', sa.INTEGER(), nullable=False),
    sa.Column('option', sa.VARCHAR(length=50), nullable=False),
    sa.Column('count', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('counselor_chat_room',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('counselor_id', sa.INTEGER(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['counselor_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
