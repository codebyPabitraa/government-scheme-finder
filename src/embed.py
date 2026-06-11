# pyrefly: ignore [missing-import]
import json
import os
# pyrefly: ignore [missing-import]
from langchain_community.vectorstores import Chroma
# pyrefly: ignore [missing-import]
from langchain_community.embeddings import HuggingFaceEmbeddings
# pyrefly: ignore [missing-import]
from langchain_core.documents import Document

def create_vectorstore():
    # Load processed schemes
    with open("data/processed/schemes_processed.json", "r", encoding="utf-8") as f:
        schemes = json.load(f)

    # Convert to documents
    docs = []
    for scheme in schemes:
        doc = Document(
            page_content=scheme["text"],
            metadata=scheme["metadata"]
        )
        docs.append(doc)

    print(f"Creating embeddings for {len(docs)} schemes...")

    # Load embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # Create and persist vectorstore
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="embeddings"
    )

    print("Vectorstore created successfully")
    return vectorstore

if __name__ == "__main__":
    create_vectorstore()