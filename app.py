import os
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import OpenAIEmbeddings
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()

vector_store_address: str = os.getenv("AZURE_SEARCH_ENDPOINT")
vector_store_password: str = os.getenv("AZURE_SEARCH_ADMIN_KEY")


index_name: str = "langchain-vector-demo"
vector_store: AzureSearch = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=vector_store_password,
    index_name=index_name,
    embedding_function=embeddings.embed_query,
)


def project_idea(query, k=4):
    docs = vector_store.similarity_search(
    query=query,
    k=k,
    search_type="similarity",
    )
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

#print(project_idea(query="Suggest me a project for AZ-104"))