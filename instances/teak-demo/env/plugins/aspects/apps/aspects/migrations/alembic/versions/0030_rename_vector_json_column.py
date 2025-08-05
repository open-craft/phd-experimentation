"""
As part of the Ralph 4.0 upgrade, we need to rename "event_json" to "event".

Later we've removed all references to the JSON columns and
allow_experimental_object_type since they have been removed from ClickHouse and cause
various errors.
"""
from alembic import op


revision = "0030"
down_revision = "0029"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '' " if "" else ""
engine = "ReplicatedReplacingMergeTree" if "" else "ReplacingMergeTree"


def upgrade():
    op.execute(
        f"""
        ALTER TABLE  openedx.xapi_events_all 
        {on_cluster} 
        RENAME COLUMN event_str to event;
        """
    )


def downgrade():
    op.execute(
        f"""
        ALTER TABLE  openedx.xapi_events_all 
        {on_cluster} 
        RENAME COLUMN event TO event_str;
        """
    )