from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '' " if "" else ""
engine = "ReplicatedMergeTree" if "" else "MergeTree"


def upgrade():
    op.execute(
        f"""
        -- Raw table that Ralph writes to
        CREATE TABLE IF NOT EXISTS xapi.xapi_events_all
        {on_cluster} 
        (      
            event_id UUID NOT NULL,
            emission_time DateTime64(6) NOT NULL,
            event String NOT NULL,
            event_str String NOT NULL
        ) ENGINE {engine}
        ORDER BY (emission_time, event_id)
        PRIMARY KEY (emission_time, event_id);
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS xapi.xapi_events_all"
        f"{on_cluster};"
    )