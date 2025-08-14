import typer
from gfr.utils.command_helpers import start_new_task

app = typer.Typer(name="bugfix", help="Start a new bugfix by creating an issue and a branch.", no_args_is_help=True)

@app.callback(invoke_without_command=True)
def bugfix(
    microservice_name: str = typer.Argument(..., help="The target service (use '.' for parent, '-' for last used)."),
    status: str = typer.Argument(..., help="start or finish."),
    bug_name: str = typer.Argument(..., help="The name of the bug (e.g., 'Logout Button Broken').")
):
    """
    Starts a new bugfix workflow.
    """
    start_new_task("bugfix", microservice_name, bug_name)
