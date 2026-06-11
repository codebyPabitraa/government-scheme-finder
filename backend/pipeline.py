# pyrefly: ignore [missing-import]
from langchain_community.vectorstores import Chroma
# pyrefly: ignore [missing-import]
from langchain_community.embeddings import HuggingFaceEmbeddings
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.llm import get_llm_response

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vectorstore = Chroma(
        persist_directory="embeddings",
        embedding_function=embeddings
    )
    return vectorstore

def retrieve_schemes(query: str, k: int = 5):
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search(query, k=k)
    return results

def rag_pipeline(user_query: str):
    # Retrieve relevant schemes
    results = retrieve_schemes(user_query)

    # Build context
    context = ""
    for r in results:
        context += r.page_content + "\n\n"

    # Build prompt
    prompt = f"""
You are a helpful Indian government scheme advisor.
Based on the following scheme information, answer the user's query in simple and clear language.
List all relevant schemes with their key benefits and eligibility.

Context:
{context}

User Query: {user_query}

Answer:
"""
    response = get_llm_response(prompt)
    return response

if __name__ == "__main__":
    query = "I am a farmer with 1 hectare land and income of 1.5 lakh. What schemes can I get?"
    print(rag_pipeline(query))