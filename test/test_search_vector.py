import unittest
from unittest.mock import MagicMock
from python--demo import AzureSearchClient

class TestAzureSearchClient(unittest.TestCase):

    def test_search(self):
        # Mock the SearchClient and its result
        mock_client = MagicMock()
        mock_search_results = [
            {'@search.score': 0.8, 'source': 'source1'},
            {'@search.score': 0.6, 'source': 'source2'},
            {'@search.score': 0.4, 'source': 'source3'}
        ]
        mock_client.search.return_value = mock_search_results

        # Create an instance of AzureSearchClient
        search_client = AzureSearchClient(
            service_endpoint="example_endpoint", api_key="example_api_key", index_name="example_index_name"
        )
        search_client.client = mock_client

        # Call the search method
        query = "example_query"
        top = 10
        threshold = 0.5
        search_parameters = {"include_total_count": True, "top": top, "skip": 0, "query_type": "full"}
        formatted_results = search_client.search(query, top, threshold, search_parameters)

        # Verify the formatted results
        self.assertEqual(len(formatted_results), 1)
        self.assertEqual(formatted_results[0]["score"], 0.8)
        self.assertEqual(formatted_results[0]["source"], "source1")

if __name__ == '__main__':
    unittest.main()
