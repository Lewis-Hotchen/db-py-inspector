from decimal import Decimal

from rich.console import Console
from rich.table import Table
from datetime import date
import json

console = Console()


class JsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, date):
            return str(obj)
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def print_table(columns: [], data):
    table = Table(*columns)

    for row in data:
        row_data = []
        for field in row:
            row_data.append((str(field)))
        table.add_row(*row_data)

    console.print(table)
