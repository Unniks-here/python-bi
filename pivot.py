import pandas as pd
from typing import Iterable


def create_pivot_table(
    rows: list[dict],
    index: Iterable[str] | None,
    columns: Iterable[str] | None,
    values: Iterable[str] | None,
    aggfunc: str = "sum",
) -> pd.DataFrame:
    """Return a pivot table DataFrame from row dictionaries."""
    df = pd.DataFrame(rows)
    pivot = pd.pivot_table(
        df,
        index=list(index) if index else None,
        columns=list(columns) if columns else None,
        values=list(values) if values else None,
        aggfunc=aggfunc,
        fill_value=0,
    )
    pivot.reset_index(inplace=True)
    return pivot
