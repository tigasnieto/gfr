import typer
from gfr.utils.command_helpers import start_new_task

app = typer.Typer(name="feature", help="Start a new feature by creating an issue and a branch.", no_args_is_help=True)

@app.callback(invoke_without_command=True)
def feature(
    microservice_name: str = typer.Argument(..., help="The target service (use '.' for parent, '-' for last used)."),
    status: str = typer.Argument(..., help="start or finish."),
    feature_name: str = typer.Argument(..., help="The name of the feature (e.g., 'Login Page').")
):
    """
    Starts a new feature workflow.
    """
    start_new_task("feature", microservice_name, feature_name)
