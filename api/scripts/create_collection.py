import json
import chromadb
from chromadb.config import Settings
from chromadb import Client
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from sentence_transformers import SentenceTransformer

def load_prepare_data(FILE_PATH: str) -> tuple:
    """
    Load data from a JSON file and prepare it for embedding.
    Args:
        FILE_PATH (str): Path to the JSON file from the current directory.
    Returns:
        tuple: tuple containing documents, metadatas, and ids.
    """
    # Load
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not data:
        raise ValueError("File empty or not found")
    # Prepare
    documents = [item["reponse"] for item in data]
    metadatas = [{"question": item["question"]} for item in data]
    ids = [f"id_{i}" for i in range(len(data))]

    return documents, metadatas, ids

def vectorize_to_chromaDB(MODEL_NAME:str, documents: list, metadatas: list, ids: list) -> None:
    """
    Vectorize documents and store them in ChromaDB.
    Args:
        documents (list): List of documents to vectorize.
        metadatas (list): List of metadata for each document.
        ids (list): List of IDs for each document.
    """
    # Vectorization
    embedding_function = SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)

    # Initialize ChromaDB with persistence
    client = chromadb. PersistentClient()
    try:
        # Create a new collection
        print("Creating new collection...")
        collection=client.create_collection(name="mohamed_rag", embedding_function=embedding_function) # type: ignore
    except Exception as e:
        # If the collection already exists replace it
        print("Collection already exists, replacing it...")
        client.delete_collection("mohamed_rag")
        collection=client.create_collection(name="mohamed_rag", embedding_function=embedding_function) # type: ignore
        print("Collection created successfully.")
        
    # Add vectorized documents
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    return None
