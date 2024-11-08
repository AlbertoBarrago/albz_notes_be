"""empty message

Revision ID: bbf1b19c3cdb
Revises: 7f5c8d095e47
Create Date: 2024-11-08 12:45:23.271982

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbf1b19c3cdb'
down_revision: Union[str, None] = '7f5c8d095e47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
