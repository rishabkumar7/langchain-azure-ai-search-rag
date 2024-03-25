# Import required modules
import os
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings()

vector_store_address: str = os.getenv("AZURE_SEARCH_ENDPOINT")
vector_store_password: str = os.getenv("AZURE_SEARCH_ADMIN_KEY")

# Initialize AzureSearch with the endpoint, key, index name, and embedding function
index_name: str = "langchain-vector-demo"
vector_store: AzureSearch = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=vector_store_password,
    index_name=index_name,
    embedding_function=embeddings.embed_query,
)


def project_idea(certification, level, k=4):
    """
    This function takes a query and an optional parameter k, performs a similarity search on the vector store, joins the page content of the returned documents, invokes the language model with the query and the documents, and returns the response from the language model.
    
    Parameters:
    query (str): The question to ask the language model.
    k (int, optional): The number of similar documents to return. Defaults to 4.

    Returns:
    str: The response from the language model.
    """

    # Perform a similarity search on the vector store
    docs = vector_store.similarity_search(
    query=certification,
    k=k,
    search_type="similarity",
    )
    # Join the page content of the returned documents
    docs = " ".join([d.page_content for d in docs])

    llm = OpenAI()

    prompt = PromptTemplate(
        input_variables=["certification", "level", "docs"],
        template="""
        You are a helpful cloud instructor that provides cloud project ideas about Microsoft Azure Certifications based on the certification guide.
        
        Give me a project idea for certification: {certification} of the level: {level}
        By searching the following certification guide: {docs}
        
        Only use the factual information from the guide to provide the project idea.
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        
        Your answers should be verbose and detailed. Include a Project Name, Project Description, list of Services Used and Steps to make the project. Make sure your response is in markdown format like:

        ### Project Name:
        Project Description:
        Services Used:
        - Service 1
        - Service 2
        #### Steps:
        - Step 1
        - Step 2
        """,
    )
    
    chain = prompt | llm
    
    response = chain.invoke({"certification":certification, "level":level, "docs":docs})
    
    #response = response.replace("\n", "")
    print (response)
    return response

# Test the function with a query
#print(project_idea(query="How much experience do I need for AZ-104"))