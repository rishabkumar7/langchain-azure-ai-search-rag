import os

from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.document_loaders import TextLoader

from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()


"""
List of URLs for the certification knowledge base. This includes the study guides for the most popular cloud certifications:
1. Microsoft Certified Azure Administrator Associate AZ-104
2. Microsoft Certified Azure Developer Associate AZ-204
3. Microsoft Certified Azure Solutions Architect Expert AZ-305
4. Microsoft Certified DevOps Engineer Expert AZ-400
"""

urls = [
    'https://learn.microsoft.com/en-us/certifications/resources/study-guides/az-104',
    'https://learn.microsoft.com/en-us/certifications/resources/study-guides/az-204',
    'https://learn.microsoft.com/en-us/certifications/resources/study-guides/az-305',
    'https://learn.microsoft.com/en-us/certifications/resources/study-guides/az-400',
]

# Configure vector store settings
vector_store_address: str = os.getenv("AZURE_SEARCH_ENDPOINT")
vector_store_password: str = os.getenv("AZURE_SEARCH_ADMIN_KEY")


index_name: str = "langchain-vector-demo"
vector_store: AzureSearch = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=vector_store_password,
    index_name=index_name,
    embedding_function=embeddings.embed_query,
)

loader = UnstructuredURLLoader(urls=urls)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

vector_store.add_documents(documents=docs)

# Perform a similarity search
docs = vector_store.similarity_search(
    query="Azure Administrator",
    k=3,
    search_type="similarity",
)
print(docs[0].page_content)


# Perform a vector similarity search with relevance scores
docs_and_scores = vector_store.similarity_search_with_relevance_scores(
    query="What are the skills for Azure Administrator",
    k=4,
    score_threshold=0.80,
)
from pprint import pprint

pprint(docs_and_scores)
