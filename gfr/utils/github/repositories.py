from github import Github, GithubException, Organization, Repository

# We can keep the custom error here or move it to a shared exceptions file
class GitHubError(Exception):
    pass

class RepositoryManager:
    def __init__(self, gh: Github, org: Organization):
        self._gh = gh
        self._org = org

    def create(self, name: str, description: str, private: bool, readmefile: bool = True) -> 'Repository':
        """Creates a new repository in the configured organization."""
        try:
            repo = self._org.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=readmefile,
            )
            return repo
        except GithubException as e:
            if e.status == 422:
                raise GitHubError(f"Repository '{name}' likely already exists.\nfull text error:\n{e})")
            else:
                raise GitHubError(f"An API error occurred: {e.data.get('message', 'Unknown error')}")
            
    def get(self, name: str) -> Repository.Repository:
        """
        Retrieves a single repository by its name.

        Args:
            name (str): The name of the repository to retrieve.

        Returns:
            The Repository object from PyGithub.

        Raises:
            GitHubError: If the repository is not found.
        """
        try:
            return self._org.get_repo(name)
        except GithubException as e:
            if e.status == 404:
                raise GitHubError(f"Repository '{name}' not found in organization '{self._org.login}'.")
            else:
                raise GitHubError(f"Failed to get repository '{name}'. Details: {e.data.get('message', 'Unknown error')}")