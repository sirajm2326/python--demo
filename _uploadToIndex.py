from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.storage.blob import BlobServiceClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import os
def upload_text_chunks_to_azure_search(text, search_service_endpoint, search_service_api_key, index_name, document_source_url, chunk_size=5000, chunk_overlap=100):
    """
    Reads text from a file, splits it into chunks, and uploads the chunks to an Azure Search service.

    Parameters:
    - file_path: Path to the text file to be read.
    - search_service_endpoint: Endpoint URL of the Azure Search service.
    - search_service_api_key: API key for the Azure Search service.
    - index_name: Name of the index in the Azure Search service where documents will be uploaded.
    - document_source_url: URL of the document source to be included in the uploaded data.
    - chunk_size: Size of each text chunk (default is 5000 characters).
    - chunk_overlap: Number of characters to overlap between chunks (default is 100 characters).
    """
    credentials = AzureKeyCredential(search_service_api_key)
    client = SearchClient(search_service_endpoint, index_name, credential=credentials)

    

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len)
    chunks = text_splitter.split_text(text)

    # Upload chunks to Azure Search
    for index, chunk in enumerate(chunks):
        data = {
            "id": str(index + 1),
            "data": chunk,
            "source": document_source_url
        }
        return client.upload_documents(documents=[data])

# Example usage:

# search_service_endpoint = os.getenv("SEARCH_SERVICE_ENDPOINT")
# search_service_api_key = os.getenv("SEARCH_SERVICE_API_KEY")
# index_name = os.getenv("INDEX_NAME")
# document_source_url = "https://talentsearchsa.blob.core.windows.net/talentsearchcontainer/10001727.pdf"
# upload_text_chunks_to_azure_search(file_path, search_service_endpoint, search_service_api_key, index_name, document_source_url)
