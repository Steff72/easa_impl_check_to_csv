import os
import openai
import chromadb
from chromadb.config import Settings

def init_chroma(sections: dict[str, str]) -> chromadb.api.models.Collection:
    """
    Initialize an in-memory Chroma collection, compute OpenAI embeddings for each section,
    and index the given document sections by IDs, embeddings, documents, and metadatas.
    Returns the Chroma Collection object.
    """
    # Set OpenAI API key and model
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # Prepare lists for ids, texts, embeddings, metadatas
    ids = []
    docs = []
    embeddings = []
    metadatas = []

    # Compute embeddings for each section using the new OpenAI API v1
    for sec_id, sec_text in sections.items():
        resp = openai.embeddings.create(
            model=model,
            input=sec_text
        )
        # Extract the embedding vector
        embedding = resp.data[0].embedding

        ids.append(sec_id)
        docs.append(sec_text)
        embeddings.append(embedding)
        metadatas.append({"sec_id": sec_id})

    # Create an in-memory Chroma client (DuckDB+Parquet backend)
    settings = Settings(chroma_db_impl="duckdb+parquet", persist_directory=None)
    client = chromadb.Client(settings=settings)

    # Create or clear the 'omd_sections' collection
    try:
        coll = client.get_collection(name="omd_sections")
        coll.delete(where={})
    except Exception:
        coll = client.create_collection(name="omd_sections")

    # Add entries with precomputed embeddings
    coll.add(
        ids=ids,
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return coll

def search_candidates(
    collection: chromadb.api.models.Collection,
    query_text: str,
    threshold: float,
    max_results: int
) -> list[str]:
    """
    Query the Chroma collection for up to `max_results` nearest neighbors,
    then return those section IDs whose similarity (distance) ≥ threshold.
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=max_results,
        include=["metadatas", "distances"]
    )
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    candidates: list[str] = []
    for md, dist in zip(metadatas, distances):
        if dist >= threshold:
            candidates.append(md["sec_id"])

    return candidates