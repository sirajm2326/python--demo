import unittest
from unittest.mock import MagicMock
from python--demo import upload_text_chunks_to_azure_search

class TestUploadTextChunksToAzureSearch(unittest.TestCase):

    def test_upload_text_chunks_to_azure_search(self):
        # Mock the SearchClient
        mock_client = MagicMock()
        mock_upload_documents = MagicMock()
        mock_client.upload_documents = mock_upload_documents

        # Define test parameters
        text = "This is a test text."
        search_service_endpoint = "example_endpoint"
        search_service_api_key = "example_api_key"
        index_name = "example_index_name"
        document_source_url = "example_document_url"
        chunk_size = 5
        chunk_overlap = 1

        # Call the function to be tested
        upload_text_chunks_to_azure_search(
            text=text,
            search_service_endpoint=search_service_endpoint,
            search_service_api_key=search_service_api_key,
            index_name=index_name,
            document_source_url=document_source_url,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            client=mock_client
        )

        # Verify that upload_documents is called with the correct data
        expected_chunks = ['This ', 'is a ', 'test ', 'text.']
        expected_documents = [
            {"id": "1", "data": "This ", "source": "example_document_url"},
            {"id": "2", "data": "is a ", "source": "example_document_url"},
            {"id": "3", "data": "test ", "source": "example_document_url"},
            {"id": "4", "data": "text.", "source": "example_document_url"}
        ]
        mock_upload_documents.assert_called_once_with(documents=expected_documents)

if __name__ == '__main__':
    unittest.main()
