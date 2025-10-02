
import frontmatter

from github_docs.github import GitHubRepo
from common.chunking import chunk_documents
from minsearch import Index


def read_data() -> dict[str, str]:
    repo_owner = "DataTalksClub"
    repo_name = "faq"

    allowed_extensions = {"md", "mdx"}

    def only_de_zoomcamp(filepath: str) -> bool:
        if "/data-engineering-zoomcamp" in filepath:
            return True
        return False

    # Download and read repository data
    print("Downloading repository data...")

    data_raw = GitHubRepo(
        repo_owner,
        repo_name,
        allowed_extensions=allowed_extensions,
        filename_filter=only_de_zoomcamp,
    ).read()


    data_parsed = []

    for f in data_raw:
        post = frontmatter.loads(f.content)
        data = post.to_dict()
        data_parsed.append(data)

    print(f"Downloaded {len(data_raw)} files from the repository.")
    return data_parsed





