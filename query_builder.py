from typing import Iterable, Sequence


def build_query(
    table: str,
    columns: Sequence[str] | None = None,
    where: str | None = None,
    aggregates: Sequence[str] | None = None,
    group_by: Sequence[str] | None = None,
) -> str:
    """Construct a SQL SELECT query from provided parts."""
    select_parts: list[str] = []
    if columns and columns != ["*"]:
        select_parts.extend(columns)
    else:
        select_parts.append("*")
    if aggregates:
        select_parts.extend(aggregates)

    select_clause = ", ".join(select_parts)
    query = f"SELECT {select_clause} FROM {table}"
    if where:
        query += f" WHERE {where}"
    if group_by:
        query += f" GROUP BY {', '.join(group_by)}"
    return query
