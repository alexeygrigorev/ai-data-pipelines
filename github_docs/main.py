import frontmatter
from typing import List, Dict, Any

from rich.console import Console
from rich.progress import track

from github_docs.github import GithubRepositoryDataReader, RawRepositoryFile
from common.indexing import index_documents
from common.interactive import InteractiveSearch


CONSOLE = Console()


def read_github_data(repo_owner: str, repo_name: str) -> List[RawRepositoryFile]:
    allowed_extensions = {"md", "mdx"}

    def only_de_zoomcamp(filepath: str) -> bool:
        return "/data-engineering-zoomcamp" in filepath

    CONSOLE.print("📥 [bold blue]Downloading repository data...[/bold blue]")

    reader = GithubRepositoryDataReader(
        repo_owner,
        repo_name,
        allowed_extensions=allowed_extensions,
        filename_filter=only_de_zoomcamp,
    )
    
    return reader.read()


def parse_data(data_raw: List[RawRepositoryFile]) -> List[Dict[str, Any]]:
    CONSOLE.print("📄 [bold blue]Parsing documents...[/bold blue]")

    data_parsed = []
    for f in track(data_raw, description="Processing files..."):
        post = frontmatter.loads(f.content)
        data = post.to_dict()
        data['filename'] = f.filename
        data_parsed.append(data)

    return data_parsed


def index_faq_data():
    repo_owner = "DataTalksClub"
    repo_name = "faq"

    data_raw = read_github_data(repo_owner, repo_name)
    documents = parse_data(data_raw)

    CONSOLE.print("🔍 [bold blue]Creating search index...[/bold blue]")

    index = index_documents(
        documents,
        chunk=True,
        chunking_params={"size": 2000, "step": 1000},
    )

    return index


class GitHubFAQSearch(InteractiveSearch):
    """Interactive search for DataTalks Club FAQ documents."""
    
    def load_data(self) -> Any:
        """Load and index FAQ data."""
        index = index_faq_data()
        CONSOLE.print(f"[green]✅ Successfully indexed {len(index.docs)} documents![/green]")
        return index

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search documents using the index."""
        return self.index.search(query)


def main():
    """Main interactive FAQ search application."""

    app = GitHubFAQSearch(
        console=CONSOLE,
        app_title="DataTalks Club FAQ Search",
        app_description="Interactive search through DataTalks Club FAQ documents",
        sample_questions=[
            "How do I run Postgres locally?",
            "How to install Docker?",
            "What are the system requirements?", 
            "How to set up the environment?",
            "How to troubleshoot installation issues?",
            "Where can I find course materials?",
            "How to submit homework?",
            "How to connect to database?"
        ]
    )
    app.run()


if __name__ == "__main__":
    main()