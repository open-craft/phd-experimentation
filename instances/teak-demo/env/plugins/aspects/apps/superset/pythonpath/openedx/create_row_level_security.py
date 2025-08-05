from superset.connectors.sqla.models import (
    RLSFilterRoles,
    RowLevelSecurityFilter,
    SqlaTable,
)
from superset.extensions import security_manager
from superset.migrations.shared.security_converge import Role

session = security_manager.get_session()

## https://docs.preset.io/docs/row-level-security-rls

XAPI_SCHEMA = "xapi"
DBT_SCHEMA = "reporting"
EVENT_SINK_SCHEMA = "event_sink"


SECURITY_FILTERS = [
    {
        "name": f"can_view_courses_{XAPI_SCHEMA}",
        "schema": XAPI_SCHEMA,
        "exclude": [],
        "role_name": "Instructor",
        "group_key": "xapi_course_id",
        "clause": '{{can_view_courses(current_username(), "splitByChar(\'/\', course_id)[-1]")}}',
        "filter_type": "Regular"
    },
    {
        "name": f"can_view_courses_{EVENT_SINK_SCHEMA}",
        "schema": EVENT_SINK_SCHEMA,
        "exclude": ["user_pii"],
        "role_name": "Instructor",
        "group_key": "xapi_course_id",
        "clause": '{{can_view_courses(current_username(), "course_key")}}',
        "filter_type": "Regular"
    },
    {
        "name": f"can_view_courses_{DBT_SCHEMA}",
        "schema": DBT_SCHEMA,
        "exclude": [],
        "role_name": "Instructor",
        "group_key": "xapi_course_id",
        "clause": '{{can_view_courses(current_username(), "course_key")}}',
        "filter_type": "Regular"
    },
]



def create_rls_filters():
    for security_filter in SECURITY_FILTERS:
        # Fetch the table we want to restrict access to
        (
            name,
            schema,
            exclude,
            role_name,
            group_key,
            clause,
            filter_type,
        ) = security_filter.values()
        tables = (
            session.query(SqlaTable)
            .filter(SqlaTable.schema == schema)
            .filter(SqlaTable.table_name.not_in(exclude))
            .all()
        )
        print(f"Creating RLS filter {name} for {schema} schema")

        role = session.query(Role).filter(Role.name == role_name).first()
        assert role, f"{role_name} role doesn't exist yet?"
        # See if the Row Level Security Filter already exists
        rlsf = (
            session.query(RowLevelSecurityFilter)
            .filter(RowLevelSecurityFilter.group_key == group_key)
            .filter(RowLevelSecurityFilter.name == name)
        ).first()
        # If it doesn't already exist, create one
        if not rlsf:
            rlsf = RowLevelSecurityFilter()
        # Sync the fields to our expectations
        rlsf.filter_type = filter_type
        rlsf.group_key = group_key
        rlsf.tables = tables
        rlsf.clause = clause
        rlsf.name = name

        session.add(rlsf)
        session.commit()
        # Add the filter role if needed
        rls_filter_roles = (
            session.query(RLSFilterRoles)
            .filter(RLSFilterRoles.c.role_id == role.id)
            .filter(RLSFilterRoles.c.rls_filter_id == rlsf.id)
        )

        if not rls_filter_roles.count():
            session.execute(
                RLSFilterRoles.insert(), [dict(role_id=role.id, rls_filter_id=rlsf.id)]
            )
            session.commit()

    print("Successfully create row-level security filters.")