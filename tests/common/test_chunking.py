"""
Tests for common.chunking module.

This module contains unit tests for the document chunking functionality,
including sliding window operations and document chunking.
"""

import pytest
from common.chunking import sliding_window, chunk_documents


class TestSlidingWindow:
    """Test cases for the sliding_window function."""

    def test_sliding_window_with_string(self):
        """Test sliding window with string input."""
        result = sliding_window("hello world", size=5, step=3)
        expected = [
            {'start': 0, 'content': 'hello'},
            {'start': 3, 'content': 'lo wo'},
            {'start': 6, 'content': 'world'},
            {'start': 9, 'content': 'ld'}
        ]
        assert result == expected

    def test_sliding_window_with_list(self):
        """Test sliding window with list input."""
        result = sliding_window([1, 2, 3, 4, 5, 6], size=3, step=2)
        expected = [
            {'start': 0, 'content': [1, 2, 3]},
            {'start': 2, 'content': [3, 4, 5]},
            {'start': 4, 'content': [5, 6]}
        ]
        assert result == expected

    def test_sliding_window_exact_size(self):
        """Test sliding window when sequence length equals window size."""
        result = sliding_window("hello", size=5, step=2)
        expected = [
            {'start': 0, 'content': 'hello'},
            {'start': 2, 'content': 'llo'}
        ]
        assert result == expected

    def test_sliding_window_step_equals_size(self):
        """Test sliding window with no overlap (step equals size)."""
        result = sliding_window("abcdefgh", size=3, step=3)
        expected = [
            {'start': 0, 'content': 'abc'},
            {'start': 3, 'content': 'def'},
            {'start': 6, 'content': 'gh'}
        ]
        assert result == expected

    def test_sliding_window_step_one(self):
        """Test sliding window with maximum overlap (step=1)."""
        result = sliding_window("abcd", size=2, step=1)
        expected = [
            {'start': 0, 'content': 'ab'},
            {'start': 1, 'content': 'bc'},
            {'start': 2, 'content': 'cd'},
            {'start': 3, 'content': 'd'}
        ]
        assert result == expected

    def test_sliding_window_empty_sequence(self):
        """Test sliding window with empty sequence."""
        result = sliding_window("", size=3, step=2)
        assert result == []

    def test_sliding_window_size_larger_than_sequence(self):
        """Test sliding window when size is larger than sequence."""
        result = sliding_window("hi", size=5, step=2)
        expected = [{'start': 0, 'content': 'hi'}]
        assert result == expected

    def test_sliding_window_invalid_size(self):
        """Test sliding window with invalid size parameter."""
        with pytest.raises(ValueError, match="size and step must be positive"):
            sliding_window("hello", size=0, step=1)
        
        with pytest.raises(ValueError, match="size and step must be positive"):
            sliding_window("hello", size=-1, step=1)

    def test_sliding_window_invalid_step(self):
        """Test sliding window with invalid step parameter."""
        with pytest.raises(ValueError, match="size and step must be positive"):
            sliding_window("hello", size=3, step=0)
        
        with pytest.raises(ValueError, match="size and step must be positive"):
            sliding_window("hello", size=3, step=-1)

    def test_sliding_window_single_character(self):
        """Test sliding window with single character string."""
        result = sliding_window("a", size=1, step=1)
        expected = [{'start': 0, 'content': 'a'}]
        assert result == expected


class TestChunkDocuments:
    """Test cases for the chunk_documents function."""

    def test_chunk_documents_basic(self):
        """Test basic document chunking functionality."""
        documents = [
            {'content': 'hello world how are you', 'filename': 'doc1.txt'}
        ]
        result = chunk_documents(documents, size=10, step=5)
        
        expected = [
            {'start': 0, 'content': 'hello worl', 'filename': 'doc1.txt'},
            {'start': 5, 'content': ' world how', 'filename': 'doc1.txt'},
            {'start': 10, 'content': 'd how are ', 'filename': 'doc1.txt'},
            {'start': 15, 'content': ' are you', 'filename': 'doc1.txt'}
        ]
        assert result == expected

    def test_chunk_documents_multiple_docs(self):
        """Test chunking multiple documents."""
        documents = [
            {'content': 'first document content', 'filename': 'doc1.txt'},
            {'content': 'second doc text', 'filename': 'doc2.txt'}
        ]
        result = chunk_documents(documents, size=10, step=5)
        
        assert len(result) == 7  # 4 chunks from first doc + 3 from second
        
        # Check first document chunks
        first_doc_chunks = [chunk for chunk in result if chunk['filename'] == 'doc1.txt']
        assert len(first_doc_chunks) == 4
        
        # Check second document chunks
        second_doc_chunks = [chunk for chunk in result if chunk['filename'] == 'doc2.txt']
        assert len(second_doc_chunks) == 3

    def test_chunk_documents_custom_content_field(self):
        """Test chunking with custom content field name."""
        documents = [
            {'text': 'hello world test', 'title': 'Test Doc'}
        ]
        result = chunk_documents(documents, size=8, step=4, content_field_name='text')
        
        expected = [
            {'start': 0, 'content': 'hello wo', 'title': 'Test Doc'},
            {'start': 4, 'content': 'o world ', 'title': 'Test Doc'},
            {'start': 8, 'content': 'rld test', 'title': 'Test Doc'},
            {'start': 12, 'content': 'test', 'title': 'Test Doc'}
        ]
        assert result == expected

    def test_chunk_documents_preserve_metadata(self):
        """Test that all metadata fields are preserved in chunks."""
        documents = [
            {
                'content': 'some text here',
                'filename': 'test.txt',
                'author': 'John Doe',
                'date': '2023-01-01',
                'tags': ['important', 'test']
            }
        ]
        result = chunk_documents(documents, size=6, step=3)
        
        for chunk in result:
            assert chunk['filename'] == 'test.txt'
            assert chunk['author'] == 'John Doe'
            assert chunk['date'] == '2023-01-01'
            assert chunk['tags'] == ['important', 'test']
            assert 'start' in chunk
            assert 'content' in chunk

    def test_chunk_documents_empty_list(self):
        """Test chunking empty document list."""
        result = chunk_documents([], size=10, step=5)
        assert result == []

    def test_chunk_documents_default_params(self):
        """Test chunking with default parameters."""
        documents = [
            {'content': 'x' * 3000, 'filename': 'large.txt'}
        ]
        result = chunk_documents(documents)
        
        # Should use default size=2000, step=1000
        assert len(result) >= 2  # Should create multiple chunks
        assert len(result[0]['content']) == 2000  # First chunk should be full size
        assert result[0]['start'] == 0
        assert result[1]['start'] == 1000  # Second chunk starts at step size

    def test_chunk_documents_small_content(self):
        """Test chunking documents smaller than chunk size."""
        documents = [
            {'content': 'short', 'filename': 'small.txt'}
        ]
        result = chunk_documents(documents, size=100, step=50)
        
        expected = [
            {'start': 0, 'content': 'short', 'filename': 'small.txt'}
        ]
        assert result == expected

    def test_chunk_documents_iterator_input(self):
        """Test that the function works with iterators, not just lists."""
        def doc_generator():
            yield {'content': 'first doc', 'id': 1}
            yield {'content': 'second doc', 'id': 2}
        
        result = chunk_documents(doc_generator(), size=5, step=3)
        assert len(result) == 6  # 3 chunks from each doc
        
        # Verify content and metadata
        first_doc_chunks = [chunk for chunk in result if chunk['id'] == 1]
        second_doc_chunks = [chunk for chunk in result if chunk['id'] == 2]
        
        assert len(first_doc_chunks) == 3
        assert len(second_doc_chunks) == 3