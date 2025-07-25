from __future__ import annotations

from db import execute_query
from query_builder import build_query
from pivot import create_pivot_table
from ui import display_results, display_dataframe, export_to_excel


def prompt_list(prompt: str) -> list[str] | None:
    value = input(prompt).strip()
    if not value:
        return None
    return [v.strip() for v in value.split(',')]


def build_or_sql() -> str:
    """Return SQL query from user input or by building interactively."""
    if input("Use raw SQL query? (y/n): ").strip().lower() == "y":
        return input("SQL query: ").strip()

    table = input("Table name: ").strip()
    columns = prompt_list("Columns to select (comma separated, default *): ") or ["*"]
    aggregates = prompt_list(
        "Aggregation functions (comma separated SQL, optional): "
    )
    where = input("Filters (SQL WHERE conditions, optional): ").strip() or None
    group_by = prompt_list("Group by columns (comma separated, optional): ")

    return build_query(table, columns, where, aggregates, group_by)


def prompt_formatting_rules(df) -> list[dict]:
    """Prompt for conditional formatting rules."""
    rules: list[dict] = []
    while True:
        column = input("Conditional format column (blank to finish): ").strip()
        if not column:
            break
        if column not in df.columns:
            print("Column not found.")
            continue
        rule: dict = {"column": column}
        gt = input("  Highlight if value > (blank to skip): ").strip()
        if gt:
            try:
                rule["gt"] = float(gt)
            except ValueError:
                pass
            color = input("  Fill color hex for > (default C6EFCE): ").strip()
            if color:
                rule["gt_fill"] = color
        lt = input("  Highlight if value < (blank to skip): ").strip()
        if lt:
            try:
                rule["lt"] = float(lt)
            except ValueError:
                pass
            color = input("  Fill color hex for < (default FFC7CE): ").strip()
            if color:
                rule["lt_fill"] = color
        if "gt" in rule or "lt" in rule:
            rules.append(rule)
    return rules


def main() -> None:
    query = build_or_sql()
    print("\nExecuting query:\n", query)
    rows = execute_query(query)
    print()
    df = display_results(rows)

    if input("\nCreate pivot table? (y/n): ").strip().lower() == "y":
        index = prompt_list("Pivot index columns (comma separated): ")
        columns = prompt_list("Pivot columns (comma separated): ")
        values = prompt_list("Pivot values (comma separated): ")
        aggfunc = input("Aggregation function (sum, mean, count) [sum]: ").strip() or "sum"
        df = create_pivot_table(rows, index, columns, values, aggfunc)
        print()
        display_dataframe(df)

    export = input("\nExport to Excel? (y/n): ").strip().lower()
    if export == "y":
        path = input("File path (default result.xlsx): ").strip() or "result.xlsx"
        rules = []
        if input("Add conditional formatting? (y/n): ").strip().lower() == "y":
            rules = prompt_formatting_rules(df)
        export_to_excel(df, path, rules)
        print("Data exported to", path)


if __name__ == "__main__":
    main()

