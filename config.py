import json
import os
from typing import Annotated
from rich import print

import typer

app = typer.Typer()
config_path = os.path.join(os.path.expanduser('~'), "postgresCLI")
file_name = os.path.join(config_path, "connections.json")


@app.command()
def ls():
    get_configs()


@app.command()
def save(config_name, database, user, password, host, port):
    save_config(config_name, database, user, password, host, port)
    print("Successfully saved connection: ")
    print(get_connection_config(config_name))


@app.command()
def amend(config_name,
          database: Annotated[str, typer.Argument()] = None,
          user: Annotated[str, typer.Argument()] = None,
          password: Annotated[str, typer.Argument()] = None,
          host: Annotated[str, typer.Argument()] = None,
          port: Annotated[str, typer.Argument()] = None
          ):
    config = get_connection_config(config_name)
    properties = {
        "database": database,
        "user": user,
        "password": password,
        "host": host,
        "port": port
    }
    for k, v in properties:
        if v is None:
            continue
        config[k] = v

    save_config(*config)


def get_configs():
    configs = get_all_configs()
    print(configs)


def get_config_path():
    if not os.path.exists(config_path):
        os.makedirs(config_path)

    if not os.path.exists(file_name):
        open(file_name, 'w').close()

    return file_name


def get_all_configs():
    with open(f"{get_config_path()}", mode="r") as fp:
        text = fp.read()
        if text != "":
            existing_connections = json.loads(text)
        else:
            existing_connections = []

    return existing_connections


def save_config(config_name, database, user, password, host, port):
    connection_config = {
        "config_name": config_name,
        "config": {
            "database": database,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
        }
    }

    with open(f"{get_config_path()}", mode="r") as fp:
        text = fp.read()
        if text != "":
            existing_connections = json.loads(text)
        else:
            existing_connections = []

    with open(f"{get_config_path()}", mode="w") as fp:
        existing_connections.append(connection_config)
        fp.write(json.dumps(existing_connections))


def get_connection_config(config_name):
    with open(f"{get_config_path()}", mode="r") as fp:
        existing_connections = json.loads(fp.read())

        for connection in existing_connections:
            if connection['config_name'] == config_name:
                return connection
        else:
            return None
