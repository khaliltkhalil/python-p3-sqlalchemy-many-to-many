"""add onDelete=CASCADE for ForeignKey in reviews table

Revision ID: 68d7204dfb34
Revises: 78a39cec99b1
Create Date: 2023-08-06 14:25:49.593804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68d7204dfb34'
down_revision = '78a39cec99b1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.drop_constraint('fk_reviews_user_id_users', type_='foreignkey')
        batch_op.drop_constraint('fk_reviews_game_id_games', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_reviews_user_id_users'), 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(batch_op.f('fk_reviews_game_id_games'), 'games', ['game_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_reviews_game_id_games'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_reviews_user_id_users'), type_='foreignkey')
        batch_op.create_foreign_key('fk_reviews_game_id_games', 'games', ['game_id'], ['id'])
        batch_op.create_foreign_key('fk_reviews_user_id_users', 'users', ['user_id'], ['id'])

    # ### end Alembic commands ###
