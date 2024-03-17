from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

class AzureSearchClient:
    def __init__(self, service_endpoint, api_key, index_name):
        self.service_endpoint = service_endpoint
        self.api_key = api_key
        self.index_name = index_name
        self.credentials = AzureKeyCredential(self.api_key)
        self.client = SearchClient(self.service_endpoint, self.index_name, credential=self.credentials)

    def search(self, query,top, threshold,search_parameters=None):
        if search_parameters is None:
            search_parameters = {"include_total_count": True, "top": top, "skip": 0, "query_type": "full"}
        results = self.client.search(search_text=query, **search_parameters)
        formatted_results = []
        for result in results:
            formatted_result = {
            "score": result['@search.score'],
            "source": result['source']
            }
            if formatted_result["score"] >= threshold:
                formatted_results.append(formatted_result)
            # print(f"score: {result['@search.score']}")
            # print(f"chunk_id: {result['source']}")
        return formatted_results
# Usage
# search_service_endpoint = "https://talentsearchservice.search.windows.net"
# search_service_api_key = "MsTKDPjrGsMKszr3WYFUANkAVF3TrTWdswSfQsSxCDAzSeAjRWpD"
# index_name = "index1"

# Create an instance of AzureSearchClient
# azure_search_client = AzureSearchClient(search_service_endpoint, search_service_api_key, index_name)

# Conduct a search
# query = "SOUS CHEF Work Experience"
# azure_search_client.search(query)
