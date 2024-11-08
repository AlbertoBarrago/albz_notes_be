"""empty message

Revision ID: d6a42cb733a4
Revises: bbf1b19c3cdb
Create Date: 2024-11-08 12:48:28.220702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6a42cb733a4'
down_revision: Union[str, None] = 'bbf1b19c3cdb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
