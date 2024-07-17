import click


def edit(editor: str):
    initial_message = ""
    edited_message = click.edit(initial_message, editor, require_save=False)
    return edited_message
