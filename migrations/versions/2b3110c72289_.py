"""empty message

Revision ID: 2b3110c72289
Revises: de326ac0cdec
Create Date: 2022-08-20 22:42:38.740030

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2b3110c72289'
down_revision = 'de326ac0cdec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('comment_ibfk_1', 'comment', type_='foreignkey')
    op.drop_constraint('comment_ibfk_2', 'comment', type_='foreignkey')
    op.drop_column('comment', 'post_id')
    op.drop_column('comment', 'author_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('author_id', mysql.VARCHAR(length=100), nullable=False))
    op.add_column('comment', sa.Column('post_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('comment_ibfk_2', 'comment', 'post', ['post_id'], ['id'])
    op.create_foreign_key('comment_ibfk_1', 'comment', 'user', ['author_id'], ['id'])
    # ### end Alembic commands ###
