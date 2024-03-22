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


def project_idea(query, k=4):
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
    query=query,
    k=k,
    search_type="similarity",
    )
    # Join the page content of the returned documents
    docs = " ".join([d.page_content for d in docs])

    llm = OpenAI()

    prompt = PromptTemplate(
        input_variables=["query", "docs"],
        template="""
        You are a helpful cloud instructor that that can answer questions about Microsoft Azure Certifications based on the certification guide.
        
        Answer the following question: {query}
        By searching the following certification guide: {docs}
        
        Only use the factual information from the guide to answer the question.
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        
        Your answers should be verbose and detailed. If asked about a project idea, include a Project Name, Project Description, Services Used in markdown format.
        """,
    )
    
    chain = prompt | llm
    
    response = chain.invoke({"query":query, "docs":docs})
    
    response = response.replace("\n", "")
    return response

# Test the function with a query
print(project_idea(query="How much experience do I need for AZ-104"))