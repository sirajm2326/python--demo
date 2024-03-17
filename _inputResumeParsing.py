from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from google.cloud import storage
from azure.storage.blob import BlobServiceClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
# Load environment variables
#load_dotenv()

# Now replace your sensitive data with environment variables
# connection_string = os.getenv("AZURE_CONNECTION_STRING")
# key_access = os.getenv("KEY_ACCESS")
# endpoint = os.getenv("AZURE_ENDPOINT")
# key = os.getenv("AZURE_KEY")
# model_id = os.getenv("MODEL_ID")

def analyze_document_from_url(form_url, endpoint, key, model_id):
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    poller = document_analysis_client.begin_analyze_document_from_url(model_id, form_url)
    result = poller.result()
    
    # Your existing logic to handle the result
    text = ""
    for page in result.pages:
        for line in page.lines:
            text += " " + line.content
        for word in page.words:
            text += " " + word.content
    # Additional code to handle tables and other elements
            # print(text)
    return text


def initialize_blob_service(connection_string):
    """Initialize and return the BlobServiceClient."""
    #connection_string = os.getenv("AZURE_CONNECTION_STRING")
    #print(connection_string)
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_string)
    return blob_service_client


# blob_service_client = initialize_blob_service()
# container_name = "talentsearchcontainer"
# container_client = blob_service_client.get_container_client(container_name)

# formUrl = "https://talentsearchsa.blob.core.windows.net/talentsearchcontainer/3547447.pdf"
# result = analyze_document_from_url(formUrl,endpoint,key,model_id)
# print(result)






