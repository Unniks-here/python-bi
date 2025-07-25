import os
import json
import time
from flask import Flask, request, render_template_string, send_from_directory
import pandas as pd
from sqlalchemy import text

from db import get_engine, execute_query
from query_builder import build_query
from pivot import create_pivot_table
from exporter import export_excel

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def get_tables() -> list[str]:
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        )
        return [row[0] for row in result]


def get_columns(table: str) -> list[str]:
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT column_name FROM information_schema.columns WHERE table_name=:t"
            ),
            {"t": table},
        )
        return [row[0] for row in result]


INDEX_TEMPLATE = """
<!doctype html>
<title>Python BI Tool</title>
<h1>Python BI Tool</h1>
<form method="get" action="/">
    <label>Table:
        <select name="table" onchange="this.form.submit()">
            {% for t in tables %}
            <option value="{{t}}" {% if t == table %}selected{% endif %}>{{t}}</option>
            {% endfor %}
        </select>
    </label>
    <noscript><input type="submit" value="Load"/></noscript>
</form>
{% if table %}
<form method="post" action="/generate">
    <input type="hidden" name="table" value="{{table}}" />
    <h2>Columns</h2>
    <label>Select columns:</label><br>
    <select name="columns" multiple size="5">
        {% for c in columns %}
        <option value="{{c}}">{{c}}</option>
        {% endfor %}
    </select>
    <h2>Where</h2>
    <input type="text" name="where" placeholder="SQL WHERE..."/>
    <h2>Aggregates (comma separated SQL)</h2>
    <input type="text" name="aggregates"/>
    <h2>Group by</h2>
    <select name="group_by" multiple size="5">
        {% for c in columns %}
        <option value="{{c}}">{{c}}</option>
        {% endfor %}
    </select>
    <h2>Pivot</h2>
    <label>Index</label><br>
    <select name="pivot_index" multiple size="5">
        {% for c in columns %}
        <option value="{{c}}">{{c}}</option>
        {% endfor %}
    </select><br>
    <label>Columns</label><br>
    <select name="pivot_columns" multiple size="5">
        {% for c in columns %}
        <option value="{{c}}">{{c}}</option>
        {% endfor %}
    </select><br>
    <label>Values</label><br>
    <select name="pivot_values" multiple size="5">
        {% for c in columns %}
        <option value="{{c}}">{{c}}</option>
        {% endfor %}
    </select><br>
    <label>Aggregation function</label>
    <select name="aggfunc">
        <option value="sum">sum</option>
        <option value="mean">mean</option>
        <option value="count">count</option>
    </select>
    <h2>Conditional Formatting Rules (JSON)</h2>
    <textarea name="formatting" rows="5" cols="60" placeholder='[{"column": "revenue", "gt": 1000}]'></textarea>
    <br><input type="submit" value="Generate Report"/>
</form>
{% endif %}
"""


RESULT_TEMPLATE = """
<!doctype html>
<title>Report generated</title>
<p>Report generated.</p>
<a href="/downloads/{{filename}}">Download {{filename}}</a>
"""


@app.route("/", methods=["GET"])
def index():
    tables = get_tables()
    table = request.args.get("table") or (tables[0] if tables else None)
    columns = get_columns(table) if table else []
    return render_template_string(INDEX_TEMPLATE, tables=tables, table=table, columns=columns)


@app.route("/generate", methods=["POST"])
def generate():
    table = request.form.get("table")
    columns = request.form.getlist("columns")
    where = request.form.get("where") or None
    aggregates = request.form.get("aggregates")
    aggregates_list = [a.strip() for a in aggregates.split(',')] if aggregates else None
    group_by = request.form.getlist("group_by") or None

    query = build_query(table, columns or ["*"], where, aggregates_list, group_by)
    rows = execute_query(query)
    df = pd.DataFrame(rows)

    pivot_index = request.form.getlist("pivot_index") or None
    pivot_columns = request.form.getlist("pivot_columns") or None
    pivot_values = request.form.getlist("pivot_values") or None
    aggfunc = request.form.get("aggfunc") or "sum"
    if pivot_index or pivot_columns or pivot_values:
        df = create_pivot_table(rows, pivot_index, pivot_columns, pivot_values, aggfunc)

    formatting_str = request.form.get("formatting")
    try:
        formatting = json.loads(formatting_str) if formatting_str else None
    except json.JSONDecodeError:
        formatting = None

    ts = int(time.time())
    filename = f"report_{ts}.xlsx"
    path = os.path.join(DOWNLOAD_DIR, filename)
    export_excel(df, path, formatting)

    return render_template_string(RESULT_TEMPLATE, filename=filename)


@app.route('/downloads/<path:filename>')
def download(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
