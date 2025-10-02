"""
Document chunking utilities for splitting large documents into smaller, overlapping pieces.

This module provides functionality to break down documents into chunks using a sliding
window approach, which is useful for processing large texts in smaller, manageable pieces
while maintaining context through overlapping content.
"""

from typing import Any, Dict, Iterable, List


def sliding_window(
        seq: Iterable[Any],
        size: int,
        step: int
    ) -> List[Dict[str, Any]]:
    """
    Create overlapping chunks from a sequence using a sliding window approach.

    Args:
        seq: The input sequence (string or list) to be chunked.
        size (int): The size of each chunk/window.
        step (int): The step size between consecutive windows.

    Returns:
        list: A list of dictionaries, each containing:
            - 'start': The starting position of the chunk in the original sequence
            - 'content': The chunk content

    Raises:
        ValueError: If size or step are not positive integers.

    Example:
        >>> sliding_window("hello world", size=5, step=3)
        [{'start': 0, 'content': 'hello'}, {'start': 3, 'content': 'lo wo'}]
    """
    if size <= 0 or step <= 0:
        raise ValueError("size and step must be positive")

    n = len(seq)
    result = []
    for i in range(0, n, step):
        batch = seq[i:i+size]
        result.append({'start': i, 'content': batch})
        if i + size > n:
            break

    return result


def chunk_documents(
        documents: Iterable[Dict[str, str]],
        size: int = 2000,
        step: int = 1000,
        content_field_name: str = 'content'
) -> List[Dict[str, str]]:
    """
    Split a collection of documents into smaller chunks using sliding windows.

    Takes documents and breaks their content into overlapping chunks while preserving
    all other document metadata (filename, etc.) in each chunk.

    Args:
        documents: An iterable of document dictionaries. Each document must have a content field.
        size (int, optional): The maximum size of each chunk. Defaults to 2000.
        step (int, optional): The step size between chunks. Defaults to 1000.
        content_field_name (str, optional): The name of the field containing document content.
                                          Defaults to 'content'.

    Returns:
        list: A list of chunk dictionaries. Each chunk contains:
            - All original document fields except the content field
            - 'start': Starting position of the chunk in original content
            - 'content': The chunk content

    Example:
        >>> documents = [{'content': 'long text...', 'filename': 'doc.txt'}]
        >>> chunks = chunk_documents(documents, size=100, step=50)
        >>> # Or with custom content field:
        >>> documents = [{'text': 'long text...', 'filename': 'doc.txt'}]
        >>> chunks = chunk_documents(documents, content_field_name='text')
    """
    results = []

    for doc in documents:
        doc_copy = doc.copy()
        doc_content = doc_copy.pop(content_field_name)
        chunks = sliding_window(doc_content, size=size, step=step)
        for chunk in chunks:
            chunk.update(doc_copy)
        results.extend(chunks)

    return results