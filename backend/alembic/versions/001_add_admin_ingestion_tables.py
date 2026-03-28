"""Add admin ingestion tables

Revision ID: 001
Revises: 
Create Date: 2026-03-17

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from models.base import GUID

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add is_admin column to users table (if not exists)
    # Note: For SQLite, we need to handle this carefully
    try:
        op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='false'))
        op.create_index('ix_users_is_admin', 'users', ['is_admin'])
    except Exception as e:
        # Column might already exist from previous run or manual addition
        print(f"Note: is_admin column handling: {e}")
    
    # Create ingestion_logs table
    op.create_table(
        'ingestion_logs',
        sa.Column('id', GUID(), nullable=False),
        sa.Column('user_id', GUID(), nullable=False),
        sa.Column('file_name', sa.String(length=500), nullable=False),
        sa.Column('file_path', sa.String(length=1000), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('file_type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('chunk_count', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('qdrant_point_ids', sa.Text(), nullable=True),  # JSON array stored as text
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ingestion_logs_user_id', 'ingestion_logs', ['user_id'])
    op.create_index('ix_ingestion_logs_status', 'ingestion_logs', ['status'])
    op.create_index('ix_ingestion_logs_created_at', 'ingestion_logs', ['created_at'])
    
    # Create reindex_jobs table
    op.create_table(
        'reindex_jobs',
        sa.Column('id', GUID(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='queued'),
        sa.Column('total_files', sa.Integer(), nullable=False),
        sa.Column('processed_files', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('failed_files', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('current_file', sa.String(length=500), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by_user_id', GUID(), nullable=False),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_reindex_jobs_status', 'reindex_jobs', ['status'])
    op.create_index('ix_reindex_jobs_created_at', 'reindex_jobs', ['created_at'])


def downgrade() -> None:
    op.drop_index('ix_reindex_jobs_created_at', table_name='reindex_jobs')
    op.drop_index('ix_reindex_jobs_status', table_name='reindex_jobs')
    op.drop_table('reindex_jobs')
    
    op.drop_index('ix_ingestion_logs_created_at', table_name='ingestion_logs')
    op.drop_index('ix_ingestion_logs_status', table_name='ingestion_logs')
    op.drop_index('ix_ingestion_logs_user_id', table_name='ingestion_logs')
    op.drop_table('ingestion_logs')
    
    op.drop_index('ix_users_is_admin', table_name='users')
    op.drop_column('users', 'is_admin')
