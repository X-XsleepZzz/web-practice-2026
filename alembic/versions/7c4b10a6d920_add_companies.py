"""add companies and application company foreign key

Revision ID: 7c4b10a6d920
Revises: 1f8bc05f0042
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "7c4b10a6d920"
down_revision: Union[str, Sequence[str], None] = "1f8bc05f0042"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(30), nullable=False),
        sa.Column("website", sa.String(), nullable=True),
    )
    op.add_column("application", sa.Column("company_id", sa.Integer(), nullable=True))
    # Preserve exact company names; do not merge case or whitespace variants.
    op.execute(sa.text(
        "INSERT INTO companies (name) SELECT DISTINCT company FROM application"
    ))
    op.execute(sa.text(
        "UPDATE application SET company_id = companies.id "
        "FROM companies WHERE application.company = companies.name"
    ))
    op.alter_column("application", "company_id", existing_type=sa.Integer(), nullable=False)
    op.create_foreign_key(
        "fk_application_company_id_companies", "application", "companies",
        ["company_id"], ["id"], ondelete="CASCADE",
    )
    op.drop_column("application", "company")


def downgrade() -> None:
    op.add_column("application", sa.Column("company", sa.String(30), nullable=True))
    op.execute(sa.text(
        "UPDATE application SET company = companies.name "
        "FROM companies WHERE application.company_id = companies.id"
    ))
    op.alter_column("application", "company", existing_type=sa.String(30), nullable=False)
    op.drop_constraint("fk_application_company_id_companies", "application", type_="foreignkey")
    op.drop_column("application", "company_id")
    op.drop_table("companies")
