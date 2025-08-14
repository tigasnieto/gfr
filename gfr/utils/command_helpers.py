# gfr/utils/command_helpers.py
from rich.console import Console
import typer

from .git.operations import GitOperations, GitError

console = Console()

def switch_to_branch(target_branch: str):
    """
    A helper function to switch the current repository to a specified branch.
    Contains shared logic for commands like 'dev' and 'doc'.
    """
    try:
        git_ops = GitOperations()

        if not git_ops.is_git_repo():
            console.print("[bold red]Error:[/bold red] This command must be run from within a Git repository.")
            raise typer.Exit(code=1)

        current_branch = git_ops.get_current_branch()

        if current_branch == target_branch:
            console.print(f"[bold yellow]You are already on the '{target_branch}' branch.[/bold yellow]")
            raise typer.Exit()

        console.print(f"Switching to branch [bold yellow]{target_branch}[/bold yellow]...")
        git_ops.switch_branch(target_branch)
        console.print(f"✔ Successfully switched to branch [bold yellow]{target_branch}[/bold yellow].")

    except GitError as e:
        if "did not match any file(s) known to git" in str(e):
             console.print(f"[bold red]Error:[/bold red] Branch '{target_branch}' does not exist locally. Try running `git fetch` or creating it first.")
        else:
            console.print(f"\n[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Operation cancelled by user.[/bold yellow]")
        raise typer.Exit()
