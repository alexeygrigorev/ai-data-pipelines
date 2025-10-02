"""
Document indexing utilities for creating searchable indexes from document collections.

This module provides functionality to index documents using minsearch, with optional
chunking support for handling large documents.
"""

from minsearch import Index

from common.chunking import chunk_documents


def index_documents(documents, chunk: bool = False, chunking_params=None) -> Index:
    """
    Create a searchable index from a collection of documents.

    Args:
        documents: A collection of document dictionaries, each containing at least
                  'content' and 'filename' fields.
        chunk (bool, optional): Whether to chunk documents before indexing.
                               Defaults to False.
        chunking_params (dict, optional): Parameters for document chunking.
                                        Defaults to {'size': 2000, 'step': 1000}.
                                        Only used when chunk=True.

    Returns:
        Index: A fitted minsearch Index object ready for searching.

    Example:
        >>> docs = [{'content': 'Hello world', 'filename': 'doc1.txt'}]
        >>> index = index_documents(docs)
        >>> results = index.search('hello')
    """
    if chunk:
        if chunking_params is None:
            chunking_params = {'size': 2000, 'step': 1000}
        documents = chunk_documents(documents, **chunking_params)

    index = Index(
        text_fields=["content", "filename"],
    )

    index.fit(documents)
    return index
