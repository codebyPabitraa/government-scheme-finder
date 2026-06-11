# pyrefly: ignore [missing-import]
from langchain_community.vectorstores import Chroma
# pyrefly: ignore [missing-import]
from langchain_community.embeddings import HuggingFaceEmbeddings
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# pyrefly: ignore [missing-import]
from src.llm import get_llm_response

def load_vectorstore():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vectorstore = Chroma(
        persist_directory=os.path.join(BASE_DIR, "embeddings"),
        embedding_function=embeddings
    )
    return vectorstore
def retrieve_schemes(query: str, k: int = 5):
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search(query, k=k)
    return results

def rag_pipeline(user_query: str):
    results = retrieve_schemes(user_query)
    context = ""
    scheme_links = []
    for r in results:
        context += r.page_content + "\n\n"
        slug = r.metadata.get("slug", "")
        name = r.metadata.get("name", "")
        if slug:
            scheme_links.append({
                "name": name,
                "url": f"https://www.myscheme.gov.in/schemes/{slug}"
            })
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
    return {"result": response , "links": scheme_links}
if __name__ == "__main__":
    query = "I am a farmer with 1 hectare land and income of 1.5 lakh. What schemes can I get?"
    output = rag_pipeline(query)
    print(output["result"])
    print("\nScheme Links:")
    for link in output["links"]:
        print(f"{link['name']} -> {link['url']}")