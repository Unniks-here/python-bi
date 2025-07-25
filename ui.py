from __future__ import annotations

import pandas as pd

from exporter import export_excel


def display_dataframe(df: pd.DataFrame) -> None:
    """Print a pandas DataFrame in a table format."""
    if df.empty:
        print("No results.")
        return
    print(df.to_string(index=False))


def display_results(rows: list[dict]) -> pd.DataFrame:
    """Convert rows to DataFrame and display them."""
    df = pd.DataFrame(rows)
    display_dataframe(df)
    return df


def export_to_excel(df: pd.DataFrame, path: str, formatting_rules: list[dict] | None = None) -> None:
    """Export DataFrame to an Excel file."""
    export_excel(df, path, formatting_rules)
