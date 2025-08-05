from alembic import op
import sqlalchemy as sa

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '' " if "" else ""
engine = "ReplicatedMergeTree" if "" else "MergeTree"


def upgrade():
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS openedx._tracking
        {on_cluster}
        (
            `time` DateTime,
            `message` String
        )
        ENGINE {engine}
        ORDER BY time;
        """
    )
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS openedx.xapi_events_all
        {on_cluster}
        (
            event_id      UUID,
            emission_time DateTime64(6),
            event_str     String
        )
        engine = {engine}
        PRIMARY KEY (emission_time)
        ORDER BY (emission_time, event_id);
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS openedx.xapi_events_all"
        f"{on_cluster}"
    )
    op.execute(
        "DROP TABLE IF EXISTS openedx._tracking"
        f"{on_cluster}"
    )