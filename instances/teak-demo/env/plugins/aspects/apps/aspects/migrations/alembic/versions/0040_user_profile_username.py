from alembic import op
import sqlalchemy as sa

revision = "0040"
down_revision = "0039"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '' " if "" else ""
engine = (
    "ReplicatedReplacingMergeTree"
    if ""
    else "ReplacingMergeTree"
)



def upgrade():
    op.execute(
        f"""
        ALTER TABLE event_sink.user_profile
        {on_cluster}
        ADD COLUMN IF NOT EXISTS username String DEFAULT ''
        AFTER name;
        """
    )


def downgrade():
    op.execute(
        f"""
        ALTER TABLE event_sink.user_profile
        {on_cluster}
        DROP COLUMN IF EXISTS username;
        """
    )