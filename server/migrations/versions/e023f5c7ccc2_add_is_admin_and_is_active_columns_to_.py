"""Add is_admin and is_active columns to User model

Revision ID: e023f5c7ccc2
Revises: ed69ea4fe08c
Create Date: 2024-08-13 12:32:24.525360

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e023f5c7ccc2'
down_revision = 'ed69ea4fe08c'
branch_labels = None
depends_on = None


def upgrade():
    # Create new 'feedbacks' table
    op.create_table('feedbacks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('feedback', sa.Text(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['events.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Drop old 'feedback' table
    op.drop_table('feedback')
    
    # Alter 'event_organizers' table
    with op.batch_alter_table('event_organizers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('organizer_name', sa.String(), nullable=False))
        batch_op.alter_column('event_id',
            existing_type=sa.INTEGER(),
            nullable=True
        )
        batch_op.drop_constraint('event_organizers_event_id_key', type_='unique')
        batch_op.drop_constraint('event_organizers_organizer_id_key', type_='unique')
        batch_op.drop_constraint('event_organizers_organizer_id_fkey', type_='foreignkey')
        batch_op.drop_column('organizer_id')
    
    # Alter 'events' table
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('number_of_tickets', sa.Integer(), nullable=False, server_default='0'))
        batch_op.alter_column('datetime',
            existing_type=sa.TEXT(),
            type_=sa.DateTime(),
            existing_nullable=True
        )
    
    # Alter 'tickets' table
    with op.batch_alter_table('tickets', schema=None) as batch_op:
        batch_op.alter_column('ticket_number',
            existing_type=sa.INTEGER(),
            type_=sa.String(),
            existing_nullable=False
        )
        batch_op.alter_column('event_id',
            existing_type=sa.INTEGER(),
            nullable=True
        )
        batch_op.create_unique_constraint(None, ['ticket_number'])
    
    # Alter 'user_events' table
    with op.batch_alter_table('user_events', schema=None) as batch_op:
        batch_op.alter_column('user_id',
            existing_type=sa.INTEGER(),
            nullable=True
        )
        batch_op.alter_column('event_id',
            existing_type=sa.INTEGER(),
            nullable=True
        )
        batch_op.drop_constraint('user_events_event_id_key', type_='unique')
        batch_op.drop_constraint('user_events_user_id_key', type_='unique')
        batch_op.drop_column('ticket_number')
    
    # Alter 'users' table
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))


def downgrade():
    # Drop columns added in 'upgrade'
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_active')
        batch_op.drop_column('is_admin')

    # Re-add 'ticket_number' column and restore constraints in 'user_events'
    with op.batch_alter_table('user_events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ticket_number', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('user_events_user_id_key', ['user_id'])
        batch_op.create_unique_constraint('user_events_event_id_key', ['event_id'])
        batch_op.alter_column('event_id',
            existing_type=sa.INTEGER(),
            nullable=False
        )
        batch_op.alter_column('user_id',
            existing_type=sa.INTEGER(),
            nullable=False
        )
    
    # Revert changes in 'tickets' table
    with op.batch_alter_table('tickets', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('event_id',
            existing_type=sa.INTEGER(),
            nullable=False
        )
        batch_op.alter_column('ticket_number',
            existing_type=sa.String(),
            type_=sa.INTEGER(),
            existing_nullable=False
        )
    
    # Revert changes in 'events' table
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.alter_column('datetime',
            existing_type=sa.DateTime(),
            type_=sa.TEXT(),
            existing_nullable=True
        )
        batch_op.drop_column('number_of_tickets')
    
    # Revert changes in 'event_organizers' table
    with op.batch_alter_table('event_organizers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('organizer_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('event_organizers_organizer_id_fkey', 'users', ['organizer_id'], ['id'])
        batch_op.create_unique_constraint('event_organizers_organizer_id_key', ['organizer_id'])
        batch_op.create_unique_constraint('event_organizers_event_id_key', ['event_id'])
        batch_op.alter_column('event_id',
            existing_type=sa.INTEGER(),
            nullable=False
        )
        batch_op.drop_column('organizer_name')
    
    # Re-create 'feedback' table
    op.create_table('feedback',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('feedback', sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], name='feedback_event_id_fkey'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='feedback_user_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='feedback_pkey')
    )
    
    # Drop new 'feedbacks' table
    op.drop_table('feedbacks')
