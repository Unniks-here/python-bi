# Python BI Tool

A minimal Business Intelligence (BI) tool. It can be used from the command line or through a small Flask web interface. The tool connects to a PostgreSQL database using SQLAlchemy, allows you to query data dynamically, and build simple pivot tables.

## Features

- Connects to PostgreSQL using environment variable `DATABASE_URL` or default connection parameters (values can also be loaded from a `.env` file).
- Interactive prompts for table name, columns, filters, aggregation and grouping or raw SQL input.
- Supports pivot table generation with pandas.
- Displays query results in a table.
- Export results or pivot tables to a styled Excel file with optional conditional formatting.
- Optional Flask web UI with dropdowns for selecting tables and columns and downloading the styled Excel report.

## Requirements

- Python 3.8+
- `pandas`, `SQLAlchemy`, `psycopg2-binary`, `openpyxl`, and `python-dotenv`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Set the connection details via `DATABASE_URL` or standard PostgreSQL environment variables (`PGUSER`, `PGPASSWORD`, `PGHOST`, `PGPORT`, `PGDATABASE`). Then run the command-line interface or start the Flask server:

```bash
python main.py

# or run the Flask app
python app.py
```

Follow the prompts to build and execute your query. You can optionally supply a raw SQL statement. After displaying the results you may generate a pivot table and export the data to an Excel file with basic styling. When exporting you can also specify simple conditional formatting rules (e.g., highlight revenue greater than a value in green or negative values in red).
When using the Flask interface the generated Excel files are stored in the `downloads/` directory with names like `report_<timestamp>.xlsx` and can be downloaded from the result page.

