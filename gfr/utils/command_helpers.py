from rich.console import Console
import typer
from .console import get_multiline_input

from .git.operations import GitOperations, GitError
from .github.api import GitHubAPI, GitHubError
from .config import GFRConfig

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

def start_new_task(task_type: str, microservice_name: str, task_name: str):
    """
    A shared helper function to start a new feature or bugfix.
    - Creates a GitHub issue.
    - Creates and switches to a new local branch.
    """
    try:
        git_ops = GitOperations()
        github_api = GitHubAPI()
        config = GFRConfig()

        if not git_ops.is_git_repo():
            console.print("[bold red]Error:[/bold red] This command must be run from within a Git repository.")
            raise typer.Exit(code=1)

        # --- Determine target repository ---
        if microservice_name == '.':
            target_path = "."
            target_name = "root project"
            repo_name_for_github = git_ops.get_root().split('/')[-1]
        elif microservice_name == '-':
            target_path = config.get_last_used_microservice()
            if not target_path:
                console.print("[bold red]Error:[/bold red] No last used microservice found.")
                raise typer.Exit(code=1)
            target_name = target_path
            repo_name_for_github = target_path
        else:
            target_path = microservice_name
            target_name = microservice_name
            repo_name_for_github = microservice_name

        # --- Get Issue Details ---
        console.print(f"\n[bold cyan]Enter description for the {task_type} '{task_name}'.[/bold cyan] (Press [bold]Ctrl+S[/bold] on a blank line, then [bold]Enter[/bold] to finish)")
        description = get_multiline_input()
        
        labels = ["enhancement" if task_type == "feature" else "bug"]

        with console.status(f"[bold yellow]Creating {task_type} on GitHub...[/bold yellow]", spinner="dots") as status:
            # --- Create GitHub Issue ---
            status.update(f"[bold yellow]Finding repository '{repo_name_for_github}'...[/bold yellow]")
            repo = github_api.repos.get(repo_name_for_github)
            
            status.update(f"[bold yellow]Creating issue in '{repo.full_name}'...[/bold yellow]")
            issue = github_api.issues.create(repo, task_name, description, labels)
            console.print(f"✔ Created {task_type} issue [bold cyan]#{issue.number}[/bold cyan]: {issue.html_url}")

            # --- Create and Switch to Branch ---
            branch_name = f"{task_type}/{issue.number}-{task_name.lower().replace(' ', '-')}"
            status.update(f"[bold yellow]Creating and switching to branch '{branch_name}'...[/bold yellow]")
            
            git_ops.create_branch(branch_name, path=target_path)
            git_ops.switch_branch(branch_name, path=target_path)
            console.print(f"✔ Switched to new branch [bold yellow]{branch_name}[/bold yellow] in [bold cyan]{target_name}[/bold cyan].")

            config.set_last_used_microservice(target_path)

        console.print(f"\n[bold green]✔ Success![/bold green] You are ready to start working on the {task_type}.")

    except (GitError, GitHubError) as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Operation cancelled by user.[/bold yellow]")
        raise typer.Exit()