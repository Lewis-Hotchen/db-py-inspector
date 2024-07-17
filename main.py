import json
import typer
from operations import app as operation_app
from config import get_connection_config, app as config_app
from clitools import JsonEncoder
from rich import print
from editor import edit

app = typer.Typer()
app.add_typer(config_app, name="config")
app.add_typer(operation_app, name="run")


if __name__ == "__main__":
    app()
