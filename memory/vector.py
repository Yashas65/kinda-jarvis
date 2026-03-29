import chromadb
import ollama
from datetime import datetime
from pathlib import Path

PATH = Path(__file__).parent /"chroma"
client = chromadb.PersistentClient(path=str(PATH))


def get_collection(name:str):
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space":"cosine"}     # sets to measure angle , rather than distance
    )


def add_summary(collection_name:str, summary:str , metadata:dict = {}):
    col = get_collection(collection_name)
    response = ollama.embeddings(model="nomic-embed-text",prompt=summary)       # converts text -> vector
    embeddings = response["embedding"]

    doc_id = f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    col.add(
        ids=[doc_id],
        embeddings=[embeddings],
        documents=[summary],
        metadatas=[metadata],
    )
    print(f"[vector] stored :{doc_id}")


def query_summaries(collection_name:str, query:str, n_results:int = 3)->list[str]:
    col = get_collection(collection_name)

    count = col.count()
    if count == 0 :
        return []
    response = ollama.embeddings(model="nomic-embed-text",prompt=query)
    embeddings = response["embedding"]

    results = col.query(
        query_embeddings=[embeddings],
        n_results=min(n_results,count)
    )
    return results["documents"][0]
    