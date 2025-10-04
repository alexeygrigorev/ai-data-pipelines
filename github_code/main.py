
from typing import List, Dict, Any

import frontmatter
import nbformat
from nbconvert import MarkdownExporter
from nbconvert.preprocessors import ClearOutputPreprocessor


from openai import OpenAI
from petcache import PetCache

from rich.console import Console

from common.llm import OpenAIResponsesWrapper, read_prompt
from common.indexing import index_documents
from common.interactive import InteractiveSearch
from common.parallel import TqdmParallelProgress

from github_docs.github import GithubRepositoryDataReader, RawRepositoryFile


CONSOLE = Console()


def strip_code_fence(text: str) -> str:
    """Remove markdown code fence markers from text."""
    text = text.strip()

    if not text.startswith("```"):
        return text

    lines = text.splitlines()
    lines = lines[1:]

    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    return "\n".join(lines)


class NotebookMarkdownFormatter:
    """Converts Jupyter notebook content to markdown format."""

    def __init__(self):
        self.exporter = MarkdownExporter()
        self.exporter.register_preprocessor(ClearOutputPreprocessor(), enabled=True)

    def format(self, raw_notebook: str) -> str:
        nb_parsed = nbformat.reads(
            raw_notebook,
            as_version=nbformat.NO_CONVERT,
        )
        md_body, _ = self.exporter.from_notebook_node(nb_parsed)
        return md_body


class LLMCodeProcessor:

    def __init__(self, llm: OpenAIResponsesWrapper):
        self.llm = llm

    def process_notebooks(self, raw_content: str) -> str:
        """Process a Jupyter notebook using LLM."""

        instructions = read_prompt("_notebook_edit.md")

        ipynb_formatter = NotebookMarkdownFormatter()
        md_body = ipynb_formatter.format(raw_content)

        new_content = self.llm(instructions, md_body)
        new_content = strip_code_fence(new_content)

        return new_content

    def process_code(self, code: str) -> str:
        """Process code using LLM."""

        instructions = read_prompt("_code_doc.md")

        new_content = self.llm(instructions, code)
        new_content = strip_code_fence(new_content)

        return new_content


DOCUMENT_EXTENSIONS = {"md", "mdx"}
NOTEBOOK_EXTENSIONS = {"ipynb"}
CODE_EXTENSIONS = {"py", "sql", "java"}


def read_github_data() -> List[RawRepositoryFile]:
    repo_owner = "DataTalksClub"
    repo_name = "data-engineering-zoomcamp"

    allowed_extensions = DOCUMENT_EXTENSIONS | NOTEBOOK_EXTENSIONS | CODE_EXTENSIONS

    CONSOLE.print("📥 [bold blue]Downloading repository data...[/bold blue]")

    reader = GithubRepositoryDataReader(
        repo_owner,
        repo_name,
        allowed_extensions=allowed_extensions
    )

    return reader.read()


def process_file(code_processor, cache: PetCache, f):
    ext = f.filename.split(".")[-1].lower()

    if ext in NOTEBOOK_EXTENSIONS:
        if f.filename in cache:
            content = cache.get(f.filename)
        else:
            CONSOLE.print(f"Processing notebook file: {f.filename}")
            content = code_processor.process_notebooks(f.content)
            cache.set(f.filename, content)

        return {
            'content': content,
            'filename': f.filename
        }

    if ext in CODE_EXTENSIONS:
        if f.filename in cache:
            content = cache.get(f.filename)
        else:
            CONSOLE.print(f"Processing code file: {f.filename}") 
            content = code_processor.process_code(f.content)
            cache.set(f.filename, content)

        return {
            'content': content,
            'filename': f.filename
        }

    if ext in DOCUMENT_EXTENSIONS:
        post = frontmatter.loads(f.content)
        data = post.to_dict()
        data['filename'] = f.filename

    return None



def process_data(data_raw: List[RawRepositoryFile]) -> List[Dict[str, Any]]:
    CONSOLE.print("📄 [bold blue]Parsing documents...[/bold blue]")

    openai_client = OpenAI()
    llm = OpenAIResponsesWrapper(openai_client)
    code_processor = LLMCodeProcessor(llm)

    cache = PetCache("llm_cache.sqlite")

    def process(record: RawRepositoryFile):
        return process_file(code_processor, cache, record)

    # this code runs "process_file" in a loop -
    # but it uses thread pool executor, so it's 6x faster
    mapper = TqdmParallelProgress()
    processed_records = mapper.map_progress(data_raw, process)
    mapper.shutdown()

    # removing None values
    processed_records = [item for item in processed_records if item]

    return processed_records


def index_de_zoomcamp_data() -> None:
    # Download and read repository data
    CONSOLE.print("Downloading repository data...")

    raw_data = read_github_data()
    CONSOLE.print(f"Downloaded {len(raw_data)} files")

    # Process and parse the data
    data = process_data(raw_data)

    index = index_documents(
        data,
        chunk=True,
        chunking_params={"size": 2000, "step": 1000}
    )

    return index


class GitHubDEZoomcampSearch(InteractiveSearch):
    """Interactive search for DataTalks Club DE Zoomcamp documents."""

    def load_data(self) -> Any:
        """Load and index DE Zoomcamp data."""
        index = index_de_zoomcamp_data()
        CONSOLE.print(f"[green]✅ Successfully indexed {len(index.docs)} documents![/green]")
        return index


def main():
    """Main interactive DE Zoomcamp search application."""

    app = GitHubDEZoomcampSearch(
        console=CONSOLE,
        app_title="DataTalks Club DE Zoomcamp Search",
        app_description="Interactive search through DataTalks Club DE Zoomcamp documents",
        sample_questions=[
            "What is data versioning and why is it important?",
            "Explain the concept of data lineage.",
            "How to set up a data pipeline using Airflow?",
            "What are the best practices for data quality management?",
            "Describe the differences between batch and stream processing.",
            "How to optimize SQL queries for large datasets?",
            "What is the role of a data engineer in a data team?",
            "Explain the concept of ETL and ELT.",
            "How to use Docker for data engineering projects?",
            "What are some common challenges in data engineering and how to overcome them?"
        ]
    )

    app.run()


if __name__ == "__main__":
    main()