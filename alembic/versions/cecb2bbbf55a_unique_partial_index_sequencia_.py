"""unique partial index sequencia_programacao

Revision ID: cecb2bbbf55a
Revises: 7c42ae8fd5eb
Create Date: 2026-11-27 14:43:06.017042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cecb2bbbf55a'
down_revision: Union[str, Sequence[str], None] = '7c42ae8fd5eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # -- sequencia_programacao unica apenas para ordens na fila; -1 (fora da sequencia) pode repetir
    op.create_index(
        "uq_ordens_producao_sequencia_programacao",
        "ordens_producao",
        ["sequencia_programacao"],
        unique=True,
        postgresql_where=sa.text("sequencia_programacao >= 0"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("uq_ordens_producao_sequencia_programacao", table_name="ordens_producao")
