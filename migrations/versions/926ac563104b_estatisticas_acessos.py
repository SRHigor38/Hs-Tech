"""Estatísticas de páginas públicas com retenção limitada.

Revision ID: 926ac563104b
Revises: 4865ca9e0b21
"""
from alembic import op
import sqlalchemy as sa

revision = '926ac563104b'
down_revision = '4865ca9e0b21'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('acesso_pagina', sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('data', sa.Date(), nullable=False), sa.Column('pagina', sa.String(50), nullable=False),
        sa.Column('visitante', sa.String(64), nullable=False), sa.Column('visualizacoes', sa.Integer(), nullable=False),
        sa.UniqueConstraint('data', 'pagina', 'visitante', name='uq_acesso_dia_pagina_visitante'))
    op.create_index('ix_acesso_pagina_data', 'acesso_pagina', ['data'])

def downgrade():
    op.drop_index('ix_acesso_pagina_data', table_name='acesso_pagina')
    op.drop_table('acesso_pagina')
