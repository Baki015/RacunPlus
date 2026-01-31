"""change user id from int to uuid

Revision ID: 5115da2a0900
Revises: 924388aff11b
Create Date: 2026-01-27 19:51:00.533549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '5115da2a0900'
down_revision: Union[str, Sequence[str], None] = '924388aff11b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - change user.id to UUID and update foreign keys"""
    op.drop_table('analysis')
    
    op.add_column('users', sa.Column('id_new', postgresql.UUID(as_uuid=True), nullable=False))
    op.execute('UPDATE users SET id_new = gen_random_uuid()')
    
    op.drop_constraint('bills_user_id_fkey', 'bills', type_='foreignkey')
    op.drop_constraint('transaction_user_id_fkey', 'transaction', type_='foreignkey')
    
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_bills_id'), table_name='bills')
    
    op.add_column('bills', sa.Column('user_id_new', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('transaction', sa.Column('user_id_new', postgresql.UUID(as_uuid=True), nullable=True))
    
    op.execute('''UPDATE bills SET user_id_new = u.id_new 
                   FROM users u WHERE bills.user_id = u.id''')
    op.execute('''UPDATE transaction SET user_id_new = u.id_new 
                   FROM users u WHERE transaction.user_id = u.id''')
    
    op.drop_column('bills', 'user_id')
    op.drop_column('transaction', 'user_id')
    op.execute('ALTER TABLE bills RENAME COLUMN user_id_new TO user_id')
    op.execute('ALTER TABLE transaction RENAME COLUMN user_id_new TO user_id')
    op.alter_column('bills', 'user_id', nullable=False)
    op.alter_column('transaction', 'user_id', nullable=False)
    
    op.drop_column('users', 'id')
    op.execute('ALTER TABLE users RENAME COLUMN id_new TO id')
    op.execute('ALTER TABLE users ADD PRIMARY KEY (id)')
    
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_bills_id'), 'bills', ['id'], unique=False)
    
    op.create_foreign_key('bills_user_id_fkey', 'bills', 'users', ['user_id'], ['id'])
    op.create_foreign_key('transaction_user_id_fkey', 'transaction', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema"""
    pass
