import os
from typing import Any, Dict, List, Generator

import dlt

from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.auth import BearerTokenAuth
from dlt.sources.helpers.rest_client.paginators import HeaderLinkPaginator

from rich.console import Console
from minsearch import Index

from common.interactive import InteractiveSearch

CONSOLE = Console()


GITHUB_API_TOKEN = os.getenv('GITHUB_API_TOKEN')


def select_fields(data: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
    """
    Selects nested fields from a dictionary.

    Args:
        data: The source dictionary.
        fields: List of field paths (dot-separated).

    Returns:
        Dictionary with selected fields.

    Examples:
        >>> data = {'user': {'login': 'alice'}, 'state': 'open'}
        >>> fields = ['user.login', 'state']
        >>> select_fields(data, fields)
        {'user_login': 'alice', 'state': 'open'}

        >>> data = {'user': {}, 'state': 'closed'}
        >>> fields = ['user.login', 'state']
        >>> select_fields(data, fields)
        {'user_login': None, 'state': 'closed'}
    """
    result: Dict[str, Any] = {}
    for field in fields:
        keys = field.split('.')
        value = data
        try:
            for k in keys:
                value = value[k]
            result[field.replace('.', '_')] = value
        except (KeyError, TypeError):
            result[field.replace('.', '_')] = None
    return result



def dot_to_underscore(fields: List[str]) -> List[str]:
    """
    Converts dots in field names to underscores.

    Args:
        fields: List of field names (possibly dot-separated).

    Returns:
        List of field names with dots replaced by underscores.
    """
    return [f.replace('.', '_') for f in fields]


@dlt.resource
def stream_items(repo_owner: str, repo_name: str, fields: List[str]) -> Generator[Dict[str, Any], None, None]:
    """
    Streams issues from a GitHub repository.

    Args:
        repo_owner: Owner of the repository.
        repo_name: Name of the repository.

    Yields:
        Dictionary with selected issue fields.
    """
    url_prefix = 'https://api.github.com/repos'
    client = RESTClient(
        base_url=f"{url_prefix}/{repo_owner}/{repo_name}",
        auth=BearerTokenAuth(token=GITHUB_API_TOKEN),
        paginator=HeaderLinkPaginator(links_next_key="next"),
    )

    for page in client.paginate("issues"):
        for item in page:
            yield select_fields(item, fields)


def read_github_data(repo_owner: str, repo_name: str) -> List[Dict[str, Any]]:
    # Configure dlt pipeline
    pipeline = dlt.pipeline(
        pipeline_name="github",
        destination="duckdb",
        dataset_name="issues",
    )

    fields = ['url', 'user.login', 'assignee.login', 'state', 'body']

    CONSOLE.print("📥 [bold blue]Downloading GitHub issues...[/bold blue]")

    # Fetch and load issues
    info = pipeline.run(
        stream_items(repo_owner, repo_name, fields=fields),
        table_name="issues",
        write_disposition="replace"
    )

    CONSOLE.print("pipeline info:", info)

    CONSOLE.print("📄 [bold blue]Processing issues...[/bold blue]")

    # Convert to dataframe and documents
    data = pipeline.dataset().issues.df()

    fields_underscored = dot_to_underscore(fields)
    documents = data[fields_underscored].to_dict(orient='records')

    return documents


def load_data():
    repo_owner = 'pydantic'
    repo_name = 'pydantic-ai'

    documents = read_github_data(repo_owner, repo_name)

    CONSOLE.print("🔍 [bold blue]Indexing documents...[/bold blue]")

    index = Index(
        text_fields=['body'],
        keyword_fields=['state']
    )
    index.fit(documents)

    return index


class GitHubIssuesSearch(InteractiveSearch):
    """Interactive search for GitHub issues."""

    def load_data(self) -> Any:
        """Load and index GitHub issues data."""
        index = load_data()
        CONSOLE.print(f"[green]✅ Successfully indexed {len(index.docs)} documents![/green]")
        return index


def main() -> None:
    
    app = GitHubIssuesSearch(
        console=CONSOLE,
        app_title="GitHub Issues Search",
        app_description="Interactive search through GitHub issues",
        sample_questions=[
            "Streaming",
            "deepseek",
            "chat completions api",
            "How to use pydantic-ai with fastapi?",
        ],
        content_field='body',
        filename_field='url'
    )
    app.run()


if __name__ == "__main__":
    main()
