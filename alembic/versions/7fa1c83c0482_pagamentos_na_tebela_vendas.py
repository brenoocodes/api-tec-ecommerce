"""Pagamentos na tebela vendas

Revision ID: 7fa1c83c0482
Revises: c7f6325dbf30
Create Date: 2024-03-27 10:57:48.502653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fa1c83c0482'
down_revision: Union[str, None] = 'c7f6325dbf30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vendas', sa.Column('link_pagamento', sa.String(length=200), nullable=True))
    op.add_column('vendas', sa.Column('pagamento_confirmado', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vendas', 'pagamento_confirmado')
    op.drop_column('vendas', 'link_pagamento')
    # ### end Alembic commands ###
