from alembic import op
import sqlalchemy as sa

revision = "0039"
down_revision = "0038"
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
        CREATE TABLE IF NOT EXISTS event_sink.tag
        {on_cluster}
        (
            id Int32,
            taxonomy Int32,
            parent Int32,
            value String,
            external_id String,
            lineage String,
            dump_id UUID NOT NULL,
            time_last_dumped String NOT NULL
        ) ENGINE {engine}
        ORDER BY (id, time_last_dumped)
        PRIMARY KEY (id, time_last_dumped);
        """
    )

    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS event_sink.taxonomy
        {on_cluster}
        (
            id Int32,
            name String,
            dump_id UUID NOT NULL,
            time_last_dumped String NOT NULL
        ) ENGINE {engine}
        ORDER BY (id, time_last_dumped)
        PRIMARY KEY (id, time_last_dumped);
        """
    )


    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS event_sink.object_tag
        {on_cluster}
        (
            id Int32,
            object_id String,
            taxonomy Int32,
            tag Int32,
            _value String,
            _export_id String,
            lineage String,
            dump_id UUID NOT NULL,
            time_last_dumped String NOT NULL
        ) ENGINE {engine}
        ORDER BY (id, time_last_dumped)
        PRIMARY KEY (id, time_last_dumped);
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS event_sink.tag"
        f"{on_cluster};"
    )

    op.execute(
        "DROP TABLE IF EXISTS event_sink.taxonomy"
        f"{on_cluster};"
    )

    op.execute(
        "DROP TABLE IF EXISTS event_sink.object_tag"
        f"{on_cluster};"
    )