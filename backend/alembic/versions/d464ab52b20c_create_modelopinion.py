"""Create ModelOpinion

Revision ID: d464ab52b20c
Revises: 17869132fb83
Create Date: 2025-05-07 21:50:10.959375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd464ab52b20c'
down_revision: Union[str, None] = '17869132fb83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('model_opinions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prediction_id', sa.Integer(), nullable=True),
    sa.Column('disease', sa.String(), nullable=True),
    sa.Column('confidence', sa.Float(), nullable=True),
    sa.Column('box_x1', sa.Integer(), nullable=True),
    sa.Column('box_y1', sa.Integer(), nullable=True),
    sa.Column('box_x2', sa.Integer(), nullable=True),
    sa.Column('box_y2', sa.Integer(), nullable=True),
    sa.Column('model_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['prediction_id'], ['prediction.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('model_opinions')
    # ### end Alembic commands ###
