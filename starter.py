# Import required modules
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to ask questions to the language model
def ask_llm(query: str):
  """
  This function takes a query as input, invokes the language model with the query,
  and returns the response from the language model.
  
  Parameters:
  query (str): The question to ask the language model.

  Returns:
  str: The response from the language model.
  """

  # Initialize the language model
  llm = ChatOpenAI()

  response = llm.invoke(query)
  return response

print(ask_llm("Can you help me with a project idea for AZ-104?"))