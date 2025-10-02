import io
from typing import Iterable
import zipfile
from dataclasses import dataclass

import requests


@dataclass
class RawRepositoryFile:
    filename: str
    content: str


class GithubRepositoryDataReader:
    """
    Downloads and parses markdown and code files from a GitHub repository.
    """

    def __init__(self,
                repo_owner: str,
                repo_name: str,
                allowed_extensions: Iterable[str] | None = None,
                filename_filter: callable[str, bool] | None = None):
        """
        Initialize the GitHub repository data reader.
        
        Args:
            repo_owner: The owner/organization of the GitHub repository
            repo_name: The name of the GitHub repository
            allowed_extensions: Optional set of file extensions to include (e.g., {"md", "py"})
            filename_filter: Optional callable to filter files by their path
        """
        prefix = "https://codeload.github.com"
        self.url = (
            f"{prefix}/{repo_owner}/{repo_name}/zip/refs/heads/main"
        )

        if allowed_extensions is None:
            self.allowed_extensions = set()
        else:
            self.allowed_extensions = {ext.lower() for ext in allowed_extensions}

        if filename_filter is None:
            self.filename_filter = lambda filepath: True
        else:
            self.filename_filter = filename_filter

    def read(self) -> list[RawRepositoryFile]:
        """
        Download and extract files from the GitHub repository.
        
        Returns:
            List of RawRepositoryFile objects for each processed file
            
        Raises:
            Exception: If the repository download fails
        """
        resp = requests.get(self.url)
        if resp.status_code != 200:
            raise Exception(f"Failed to download repository: {resp.status_code}")

        zf = zipfile.ZipFile(io.BytesIO(resp.content))
        repository_data = self._extract_files(zf)
        zf.close()

        return repository_data

    def _extract_files(self, zf: zipfile.ZipFile) -> list[RawRepositoryFile]:
        """
        Extract and process files from the zip archive.
        
        Args:
            zf: ZipFile object containing the repository data

        Returns:
            List of RawRepositoryFile objects for each processed file
        """
        data = []

        for file_info in zf.infolist():
            filepath = self._normalize_filepath(file_info.filename)

            if self._should_skip_file(filepath):
                continue

            try:
                with zf.open(file_info) as f_in:
                    content = f_in.read().decode("utf-8", errors="ignore")
                    if content is not None:
                        content = content.strip()

                    file = RawRepositoryFile(
                        filename=filepath,
                        content=content
                    )
                    data.append(file)

            except Exception as e:
                print(f"Error processing {file_info.filename}: {e}")
                continue

        return data

    def _should_skip_file(self, filepath: str) -> bool:
        """
        Determine whether a file should be skipped during processing.
        
        Args:
            filepath: The file path to check
            
        Returns:
            True if the file should be skipped, False otherwise
        """
        filepath = filepath.lower()

        # directory
        if filepath.endswith("/"):
            return True

        # hidden file
        filename = filepath.split("/")[-1]
        if filename.startswith("."):
            return True

        ext = self._get_extension(filepath)
        if ext not in self.allowed_extensions:
            return True

        if not self.filename_filter(filepath):
            return True

        return False



    def _get_extension(self, filepath: str) -> str:
        """
        Extract the file extension from a filepath.
        
        Args:
            filepath: The file path to extract extension from
            
        Returns:
            The file extension (without dot) or empty string if no extension
        """
        filename = filepath.lower().split("/")[-1]
        if "." in filename:
            return filename.split(".")[-1]
        else:
            return ""

    def _normalize_filepath(self, filepath: str) -> str:
        """
        Removes the top-level directory from the file path inside the zip archive.
        'repo-main/path/to/file.py' -> 'path/to/file.py'
        
        Args:
            filepath: The original filepath from the zip archive
            
        Returns:
            The normalized filepath with top-level directory removed
        """
        parts = filepath.split("/", maxsplit=1)
        if len(parts) > 1:
            return parts[1]
        else:
            return parts[0]

