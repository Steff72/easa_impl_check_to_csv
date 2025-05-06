import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os


def init_chroma(sections):
    """
    Initialize Chroma client, create collection, and index document sections.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name=model
    )
    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=".chromadb"))
    try:
        coll = client.get_collection(name="omd_sections")
        coll.delete(where={})
    except Exception:
        coll = client.create_collection(name="omd_sections", embedding_function=ef)
    ids, docs, metadatas = [], [], []
    for sec_id, sec_text in sections.items():
        ids.append(sec_id)
        docs.append(sec_text)
        metadatas.append({"sec_id": sec_id})
    coll.add(ids=ids, documents=docs, metadatas=metadatas)
    return coll


def search_candidates(chroma_client, query_text, threshold, max_results):
    """
    Embed the query_text and search Chroma for up to max_results candidates,
    filtering by similarity >= threshold. Returns list of section IDs.
    """
    results = chroma_client.query(
        query_texts=[query_text],
        n_results=max_results,
        include=["metadatas", "distances"]
    )
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    return [md["sec_id"] for md, dist in zip(metadatas, distances) if dist >= threshold]