
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from _inputResumeParsing import initialize_blob_service,analyze_document_from_url
from _uploadToIndex import upload_text_chunks_to_azure_search
from _searchVector import AzureSearchClient
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/api/skills', methods=['GET'])
def get_skills():
    
    # Example response. Replace with actual logic to extract skills from resumes
    skills = ['Python', 'JavaScript', 'SQL']
    return jsonify(skills)



@app.route('/analyze-document', methods=['POST'])
def analyze_document():
    # Extract parameters from JSON payload
    data = request.json
    context = data.get('context')
    category = data.get('category')
    threshold = data.get('threshold')
    noOfMatches = data.get('noOfMatches')
    form_url = data.get('inputPath')  # Use this URL for document analysis

    # Ensure all mandatory parameters are provided
    if not all([context, category, threshold, noOfMatches, form_url]):
        return jsonify({"error": "All parameters are clearmandatory"}), 400
    
    connection_string = "DefaultEndpointsProtocol=https;AccountName=talentsearchsa;AccountKey=X5VAmu8ojrytOQ3BSV1RK3fXdDEuGCZ32OIUQhYjtxcM4r8nDIxiHnahj1P/Y8sRs8fDe1qwTUvf+AStseVw5w==;EndpointSuffix=core.windows.net"
    key_access = os.getenv("KEY_ACCESS")
    endpoint = os.getenv("AZURE_ENDPOINT")
    key = os.getenv("AZURE_KEY")
    model_id = os.getenv("MODEL_ID")
    searchServiceEndpoint = os.getenv("SEARCH_SERVICE_ENDPOINT")
    blob_service_client = initialize_blob_service(connection_string)
    container_name = "talentsearchcontainer"
    container_client = blob_service_client.get_container_client(container_name)

    formUrl = "https://talentsearchsa.blob.core.windows.net/talentsearchcontainer/3547447.pdf"
    result = analyze_document_from_url(formUrl,endpoint,key,model_id)
    searchServiceEndpoint = os.getenv("SEARCH_SERVICE_ENDPOINT")
    search_service_api_key = os.getenv("SEARCH_SERVICE_API_KEY")
    indexName=os.getenv("INDEX_NAME")

    
    upload_text_chunks_to_azure_search(result,searchServiceEndpoint,search_service_api_key,indexName,formUrl)
    search_service_endpoint = "https://talentsearchservice.search.windows.net"
    search_service_api_key = "MsTKDPjrGsMKszr3WYFUANkAVF3TrTWdswSfQsSxCDAzSeAjRWpD"


# Create an instance of AzureSearchClient
    azure_search_client = AzureSearchClient(search_service_endpoint, search_service_api_key, indexName)
    query = "SOUS CHEF Work Experience"
    responses=azure_search_client.search(context,noOfMatches,threshold)
#     formatted_results = []

# # Step 2: Iterate over each result in results
#     for result in responses:
#         # Step 3: Create a dictionary with the desired structure for each result
#         formatted_result = {
#             "score": result['@search.score'],
#             "source": result['source']
#         }
        
#         # Step 4: Append the dictionary to the list
#         formatted_results.append(formatted_result)
    return jsonify(responses)
if __name__ == '__main__':
    app.run(debug=True)