# gfr/utils/github/api.py
import os
from dotenv import load_dotenv
from github import Github, GithubException

# Import the manager and the custom exception
from .repositories import RepositoryManager, GitHubError

class GitHubAPI:
    """A wrapper for the PyGithub library to handle auth and operations."""
    def __init__(self):
        """Initializes the GitHub API client and its managers."""
        load_dotenv()
        token = os.getenv("GITHUB_TOKEN")
        self.org_name = os.getenv("GITHUB_ORGANIZATION")
        self.username = os.getenv("GITHUB_USERNAME")

        if not all([token, self.org_name, self.username]):
            raise GitHubError("Missing credentials in your .env file.")

        try:
            self._gh = Github(token)
            self._org = self._gh.get_organization(self.org_name)
        except GithubException as e:
            raise GitHubError(f"Auth/Org error: {e.data.get('message', 'Unknown error')}")

        # --- Initialize and expose managers ---
        self.repos = RepositoryManager(self._gh, self._org)
        # self.issues = IssueManager(self._gh, self._org) # You would add this later
        # self.prs = PullRequestManager(self._gh, self._org) # And this one