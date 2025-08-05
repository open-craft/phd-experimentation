"""
add a 'graded' boolean to course_block_names_dict and course_block_names
"""
from alembic import op


revision = "0017"
down_revision = "0016"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '' " if "" else ""


def drop_objects():
    # We include these drop statements here because "CREATE OR REPLACE DICTIONARY"
    # currently throws a file rename error and you can't drop a dictionary with a
    # table referring to it.
    op.execute(
        f"""
        DROP TABLE IF EXISTS event_sink.course_block_names
        {on_cluster}
        """
    )
    op.execute(
        f"""
        DROP DICTIONARY IF EXISTS event_sink.course_block_names_dict
        {on_cluster}
        """
    )


def upgrade():
    drop_objects()
    op.execute(
        f"""
        CREATE DICTIONARY event_sink.course_block_names_dict 
        {on_cluster}
        (
            location String,
            block_name String,
            course_key String,
            graded Bool
        )
        PRIMARY KEY location
        SOURCE(CLICKHOUSE(
            user 'ch_admin'
            password 'WCCxAm9AYpkR2j2NjNDJK6c0'
            db 'event_sink'
            query "with most_recent_blocks as (
                    select org, course_key, location, max(edited_on) as last_modified
                    from event_sink.course_blocks
                    group by org, course_key, location
                )
                select
                    location,
                    display_name,
                    course_key,
                    JSONExtractBool(xblock_data_json, 'graded') as graded
                from event_sink.course_blocks co
                inner join most_recent_blocks mrb on
                    co.org = mrb.org and
                    co.course_key = mrb.course_key and
                    co.location = mrb.location and
                    co.edited_on = mrb.last_modified
            "
        ))
        LAYOUT(COMPLEX_KEY_SPARSE_HASHED())
        LIFETIME(120);
        """
    )
    op.execute(
        f"""
        CREATE OR REPLACE TABLE event_sink.course_block_names
        {on_cluster}
        (
            location String,
            block_name String,
            course_key String,
            graded Bool
        ) engine = Dictionary(event_sink.course_block_names_dict)
        ;
        """
    )


def downgrade():
    drop_objects()
    op.execute(
        f"""
        CREATE DICTIONARY event_sink.course_block_names_dict 
        {on_cluster}
        (
            location String,
            block_name String,
            course_key String
        )
        PRIMARY KEY location
        SOURCE(CLICKHOUSE(
            user 'ch_admin'
            password 'WCCxAm9AYpkR2j2NjNDJK6c0'
            db 'event_sink'
            query 'with most_recent_blocks as (
                    select org, course_key, location, max(edited_on) as last_modified
                    from event_sink.course_blocks
                    group by org, course_key, location
                )
                select
                    location,
                    display_name,
                    course_key
                from event_sink.course_blocks co
                inner join most_recent_blocks mrb on
                    co.org = mrb.org and
                    co.course_key = mrb.course_key and
                    co.location = mrb.location and
                    co.edited_on = mrb.last_modified
            '
        ))
        LAYOUT(COMPLEX_KEY_SPARSE_HASHED())
        LIFETIME(120);
        """
    )
    op.execute(
        f"""
        CREATE OR REPLACE TABLE event_sink.course_block_names
        {on_cluster}
        (
            location String,
            block_name String,
            course_key String
        ) engine = Dictionary(event_sink.course_block_names_dict)
        ;
        """
    )