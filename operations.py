import json

import psycopg2
from psycopg2 import extras

import connection
from clitools import print_table, JsonEncoder
from rich import print
import typer

from config import get_connection_config
from editor import edit

app = typer.Typer()


@app.command()
def query_json(config_name: str, editor: str = "vim"):
    written_query = edit(editor)
    conn = connection.Connection(get_connection_config(config_name)['config'])
    cursor = conn.connection.cursor()
    cursor.execute(written_query)

    # Fetch all rows from database
    records = cursor.fetchall()

    records_as_dict = []
    for x in records:
        temp2 = {}
        c = 0
        for col in cursor.description:
            temp2.update({str(col[0]): x[c]})
            c = c + 1
        records_as_dict.append(temp2)

    print(json.dumps(records, cls=JsonEncoder))


@app.command()
def query(config_name: str, editor: str = "vim", limit: int = 100):
    try:
        written_query = edit(editor)
        conn = connection.Connection(get_connection_config(config_name)['config'])
        cursor = conn.connection.cursor()
        cursor.execute(written_query)
        col_names = [desc[0] for desc in cursor.description]

        # Fetch all rows from database
        records = cursor.fetchall()

        for row_count in range(0, len(records), limit):
            slice = records[row_count: row_count+limit]
            print_table(col_names, slice)
            input("Press Enter to continue...")

        cursor.close()
    except Exception as e:
        print("[bold red]Syntax error! SQL did NOT work[/bold red]")
        print(e)


@app.command()
def schema(config_name):
    conn = connection.Connection(get_connection_config(config_name)['config'])
    cursor = conn.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("""SELECT table_name
                          FROM information_schema.tables
                          WHERE table_schema != 'pg_catalog'
                          AND table_schema != 'information_schema'
                          AND table_type='BASE TABLE'
                          ORDER BY table_schema, table_name""")

    tables = cursor.fetchall()
    columns = ['table_name']
    print_table(columns, tables)
    cursor.close()
