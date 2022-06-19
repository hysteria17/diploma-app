"""empty message

Revision ID: 9726fc277db8
Revises: 
Create Date: 2022-06-19 01:48:46.949740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9726fc277db8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('source',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('sensor_id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('country', sa.String(length=128), nullable=False),
    sa.Column('country_code', sa.String(length=128), nullable=False),
    sa.Column('valid_from', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sensor_id')
    )
    op.create_table('observation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('wind_from_direction_value', sa.Float(), nullable=True),
    sa.Column('wind_speed_value', sa.Float(), nullable=True),
    sa.Column('air_temperature', sa.Float(), nullable=True),
    sa.Column('reference_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('observation')
    op.drop_table('source')
    # ### end Alembic commands ###
