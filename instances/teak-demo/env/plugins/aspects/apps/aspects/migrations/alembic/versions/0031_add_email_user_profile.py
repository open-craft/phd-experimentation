"""
Add email column to user profile table
"""
from alembic import op


revision = "0031"
down_revision = "0030"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '' " if "" else ""


def upgrade():
    op.execute(
        f"""
        ALTER TABLE event_sink.user_profile
        {on_cluster}
        ADD COLUMN IF NOT EXISTS email String DEFAULT '' 
        AFTER name;
        """
    )


def downgrade():
    op.execute(
        f"""
        ALTER TABLE event_sink.user_profile
        {on_cluster}
        DROP COLUMN IF EXISTS email;
        """
    )