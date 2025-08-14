import subprocess
import sys
import os
from .exceptions import GitError

class GitOperations:
    """
    Handles the execution of local Git commands.
    """

    def _run_command(self, command: list[str], cwd: str = "."):
        """
        A private helper to run git commands and handle errors.

        Args:
            command (list[str]): The command to execute.
            cwd (str): The working directory to run the command in.

        Raises:
            GitError: If the command fails.
        """
        try:
            # Resolve the path to an absolute path for consistency
            abs_cwd = os.path.abspath(cwd)
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=abs_cwd
            )
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                raise GitError(f"Git command failed: {command}\nError: {stderr.strip()}")
            return stdout.strip()

        except FileNotFoundError:
            raise GitError("`git` command not found. Is Git installed and in your PATH?")
        except Exception as e:
            raise GitError(f"An unexpected error occurred: {e}")

    def is_git_repo(self, path: str = ".") -> bool:
        """Checks if the given path is a Git repository."""
        abs_path = os.path.abspath(path)
        return os.path.isdir(os.path.join(abs_path, ".git"))

    def init(self, path: str = "."):
        """Initializes a new Git repository in the specified path."""
        self._run_command(["git", "init"], cwd=path)

    def add_remote(self, remote_url: str, path: str = "."):
        """Adds a new remote named 'origin'."""
        self._run_command(["git", "remote", "add", "origin", remote_url], cwd=path)

    def pull(self, branch_name: str, path: str = "."):
        """Pulls a branch from the 'origin' remote."""
        self._run_command(["git", "pull", "origin", branch_name], cwd=path)

    def create_branch(self, branch_name: str, start_point: str = "HEAD", path: str = "."):
        """Creates a new branch from a starting point."""
        self._run_command(["git", "branch", branch_name, start_point], cwd=path)

    def switch_branch(self, branch_name: str, path: str = "."):
        """Switches to an existing branch."""
        self._run_command(["git", "checkout", branch_name], cwd=path)

    def push_branch(self, branch_name: str, set_upstream: bool = False, path: str = "."):
        """Pushes a branch to the 'origin' remote."""
        cmd = ["git", "push", "origin", branch_name]
        if set_upstream:
            cmd.insert(2, "-u")
        self._run_command(cmd, cwd=path)

    def fetch(self, remote: str = "origin", path: str = "."):
        """Fetches updates from a remote repository."""
        self._run_command(["git", "fetch", remote], cwd=path)

    def clone(self, clone_url: str, repo_name: str, target_dir: str = ".") -> str:
        """
        Clones a repository into a specific target directory.
        'git clone' will create a new folder named after the repo inside the target_dir.
        """
        abs_target_dir = os.path.abspath(target_dir)
        final_repo_path = os.path.join(abs_target_dir, repo_name)

        if os.path.exists(final_repo_path):
            raise GitError(f"Destination path '{final_repo_path}' already exists.")

        try:
            os.makedirs(abs_target_dir, exist_ok=True)
        except OSError as e:
            raise GitError(f"Could not create target directory '{abs_target_dir}': {e}")

        self._run_command(["git", "clone", clone_url], cwd=abs_target_dir)
        return final_repo_path

    def add_submodule(self, repo_url: str, path: str, parent_path: str = "."):
        """Adds a new Git submodule."""
        self._run_command(["git", "submodule", "add", repo_url, path], cwd=parent_path)
        
    def add(self, files: list[str], path: str = "."):
        """Adds file contents to the index."""
        cmd = ["git", "add"] + files
        self._run_command(cmd, cwd=path)

    def commit(self, message: str, path: str = "."):
        """Records changes to the repository."""
        self._run_command(["git", "commit", "-m", message], cwd=path)