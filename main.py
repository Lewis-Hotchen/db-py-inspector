import typer
from operations import app as operation_app
from config import app as config_app

app = typer.Typer()
app.add_typer(config_app, name="config")
app.add_typer(operation_app, name="run")


if __name__ == "__main__":
    app()
