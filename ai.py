# Import required modules
import os
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

embeddings = OpenAIEmbeddings()

vector_store_address: str = os.getenv("AZURE_SEARCH_ENDPOINT")
vector_store_password: str = os.getenv("AZURE_SEARCH_ADMIN_KEY")

vector_store=AzureSearch(vector_store_address, vector_store_password, embedding_function=embeddings, index_name="langchain-vector-demo")


# Function to ask questions to the language model
def project_idea(certification, level):
  """
  This function takes a query as input, invokes the language model with the query,
  and returns the response from the language model.
  
  Parameters:
  query (str): The question to ask the language model.

  Returns:
  str: The response from the language model.
  """

  docs = vector_store.similarity_search(query=certification, k=3, search_type="similarity",)
  docs = " ".join([d.page_content for d in docs])
  # Initialize the language model
  llm = OpenAI()

  template = PromptTemplate(
    input_variables=["certification", "level", "docs"],
    template = """
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
        """
  )
  chain = llm | template
  response = chain.invoke({"certification":certification, "level":level})
  return response