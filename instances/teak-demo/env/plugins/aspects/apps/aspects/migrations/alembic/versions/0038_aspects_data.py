from alembic import op
import sqlalchemy as sa

revision = "0038"
down_revision = "0037"
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
        CREATE TABLE IF NOT EXISTS event_sink.aspects_data
        {on_cluster}
        (
            path String NOT NULL,
            content String NOT NULL,
        ) ENGINE {engine}
        PRIMARY KEY (path);
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS event_sink.aspects_data"
        f"{on_cluster};"
    )