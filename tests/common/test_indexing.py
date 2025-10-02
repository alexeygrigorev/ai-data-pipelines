"""
Tests for common.indexing module.

This module contains unit tests for the document indexing functionality,
including minsearch integration and chunking support.
"""

from minsearch import Index
from common.indexing import index_documents


class TestIndexDocuments:
    """Test cases for the index_documents function."""

    def test_index_documents_basic(self):
        """Test basic document indexing without chunking."""
        documents = [
            {'content': 'Hello world programming', 'filename': 'doc1.txt'},
            {'content': 'Python testing framework', 'filename': 'doc2.txt'}
        ]
        
        result = index_documents(documents)
        
        # Verify that we get back an Index object
        assert isinstance(result, Index)
        
        # Test that we can search the index
        search_results = result.search('programming')
        assert len(search_results) >= 1
        assert any('programming' in doc['content'] for doc in search_results)
        
        # Test searching for specific content
        python_results = result.search('Python')
        assert len(python_results) >= 1
        assert any('Python' in doc['content'] for doc in python_results)

    def test_index_documents_with_chunking(self):
        """Test document indexing with chunking enabled."""
        # Create a long document that will be chunked
        long_content = 'This is a very long document. ' * 100  # 3000+ chars
        original_docs = [
            {'content': long_content, 'filename': 'long_doc.txt'}
        ]
        
        result = index_documents(original_docs, chunk=True, chunking_params={'size': 100, 'step': 50})
        
        # Verify that we get back an Index object
        assert isinstance(result, Index)
        
        # Test that we can search the chunked index
        search_results = result.search('very long document')
        assert len(search_results) >= 1
        
        # Verify that chunks have start positions (indicating they were chunked)
        assert any('start' in doc for doc in search_results)

    def test_index_documents_custom_chunking_params(self):
        """Test document indexing with custom chunking parameters."""
        documents = [{'content': 'Test content for custom chunking parameters', 'filename': 'test.txt'}]
        custom_params = {'size': 20, 'step': 10}
        
        result = index_documents(documents, chunk=True, chunking_params=custom_params)
        
        assert isinstance(result, Index)
        
        # Test searching
        search_results = result.search('content')
        assert len(search_results) >= 1

    def test_index_documents_no_chunking_when_disabled(self):
        """Test that chunking is not performed when chunk=False."""
        documents = [{'content': 'Test document without chunking', 'filename': 'test.txt'}]
        
        result = index_documents(documents, chunk=False)
        
        assert isinstance(result, Index)
        
        # Search and verify original document structure
        search_results = result.search('document')
        assert len(search_results) >= 1
        # Should not have 'start' field since it wasn't chunked
        assert all('start' not in doc for doc in search_results)

    def test_index_documents_empty_list(self):
        """Test indexing empty document list."""
        result = index_documents([])
        
        assert isinstance(result, Index)
        
        # Search should return no results
        search_results = result.search('anything')
        assert len(search_results) == 0

    def test_index_documents_single_document(self):
        """Test indexing single document."""
        documents = [{'content': 'Single document for testing', 'filename': 'single.txt'}]
        
        result = index_documents(documents)
        
        assert isinstance(result, Index)
        
        # Test searching
        search_results = result.search('Single')
        assert len(search_results) == 1
        assert search_results[0]['filename'] == 'single.txt'

    def test_index_documents_chunking_params_none_uses_defaults(self):
        """Test that None chunking_params uses default values."""
        # Create content that's long enough to be chunked with defaults
        long_content = 'word ' * 1000  # About 5000 characters
        documents = [{'content': long_content, 'filename': 'test.txt'}]
        
        result = index_documents(documents, chunk=True, chunking_params=None)
        
        assert isinstance(result, Index)
        
        # Should be able to search and find results
        search_results = result.search('word')
        assert len(search_results) >= 1

    def test_index_documents_preserves_metadata(self):
        """Test that all document metadata is preserved in the index."""
        documents = [
            {
                'content': 'Test content with metadata',
                'filename': 'test.txt',
                'author': 'Test Author',
                'category': 'testing',
                'tags': ['test', 'metadata']
            }
        ]
        
        result = index_documents(documents)
        
        assert isinstance(result, Index)
        
        # Search and verify metadata is preserved
        search_results = result.search('content')
        assert len(search_results) >= 1
        
        doc = search_results[0]
        assert doc['filename'] == 'test.txt'
        assert doc['author'] == 'Test Author'
        assert doc['category'] == 'testing'
        assert doc['tags'] == ['test', 'metadata']

    def test_index_documents_multiple_documents(self):
        """Test indexing multiple documents and searching across them."""
        documents = [
            {'content': 'Python is a programming language', 'filename': 'python.txt'},
            {'content': 'Java is also a programming language', 'filename': 'java.txt'},
            {'content': 'JavaScript is used for web development', 'filename': 'js.txt'}
        ]
        
        result = index_documents(documents)
        
        assert isinstance(result, Index)
        
        # Test searching across all documents
        prog_results = result.search('programming')
        assert len(prog_results) == 2  # Python and Java docs
        
        # Test specific searches
        python_results = result.search('Python')
        assert len(python_results) == 1
        assert python_results[0]['filename'] == 'python.txt'
        
        js_results = result.search('JavaScript')
        assert len(js_results) == 1
        assert js_results[0]['filename'] == 'js.txt'

    def test_index_documents_search_by_filename(self):
        """Test that filename field is also searchable."""
        documents = [
            {'content': 'Some content about important topic', 'filename': 'important_document.txt'},
            {'content': 'Other content', 'filename': 'regular_file.txt'}
        ]
        
        result = index_documents(documents)
        
        # Search by content that includes the term 'important'
        filename_results = result.search('important')
        assert len(filename_results) >= 1
        assert any('important_document.txt' in doc['filename'] for doc in filename_results)

    def test_index_documents_chunking_with_custom_content_field(self):
        """Test chunking with custom content field name."""
        documents = [
            {
                'text': 'This is custom content field. ' * 50,  # Long enough to chunk
                'filename': 'custom.txt',
                'title': 'Custom Field Test'
            }
        ]
        
        chunking_params = {'size': 50, 'step': 25, 'content_field_name': 'text'}
        result = index_documents(documents, chunk=True, chunking_params=chunking_params)
        
        assert isinstance(result, Index)
        
        # Search should work and find chunked content
        search_results = result.search('custom content')
        assert len(search_results) >= 1
        
        # Verify metadata is preserved in chunks
        for doc in search_results:
            assert doc['filename'] == 'custom.txt'
            assert doc['title'] == 'Custom Field Test'
            # Should have start field from chunking
            assert 'start' in doc