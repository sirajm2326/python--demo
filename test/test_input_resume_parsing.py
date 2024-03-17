import unittest
from unittest.mock import patch, MagicMock
from python--demo import analyze_document_from_url, initialize_blob_service

class TestDocumentAnalysis(unittest.TestCase):

    @patch('python--demo.DocumentAnalysisClient')
    def test_analyze_document_from_url(self, mock_client):
        # Mock the DocumentAnalysisClient and its result
        mock_poller = MagicMock()
        mock_result = MagicMock()
        mock_result.pages = [
            MagicMock(lines=[MagicMock(content='line1'), MagicMock(content='line2')]),
            MagicMock(words=[MagicMock(content='word1'), MagicMock(content='word2')])
        ]
        mock_poller.result.return_value = mock_result
        mock_client.return_value.begin_analyze_document_from_url.return_value = mock_poller

        # Call the function to be tested
        result = analyze_document_from_url(
            form_url="example_url", endpoint="example_endpoint", key="example_key", model_id="example_model_id"
        )

        # Verify the function output
        expected_text = " line1 line2 word1 word2"
        self.assertEqual(result, expected_text)

    @patch('python--demo.BlobServiceClient')
    def test_initialize_blob_service(self, mock_blob_service):
        # Call the function to be tested
        initialize_blob_service("example_connection_string")

        # Verify that BlobServiceClient is initialized with the correct arguments
        mock_blob_service.from_connection_string.assert_called_once_with(conn_str="example_connection_string")

if __name__ == '__main__':
    unittest.main()
