# src/vector_search.py

import os
import openai
import chromadb

def init_chroma(
    sections: dict[str, str]
) -> chromadb.api.models.Collection:
    """
    Build an in-memory Chroma collection by:
    1) Computing OpenAI embeddings for each section
    2) Creating a Chroma EphemeralClient
    3) Adding the precomputed embeddings & IDs to a collection
    Returns the ready-to-query collection.
    """
    # Load OpenAI key & model
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # Prepare lists for IDs, embeddings and metadata
    ids = []
    embeddings = []
    metadatas = []

    # Compute an embedding for each section
    for sec_id, sec_text in sections.items():
        resp = openai.embeddings.create(
            model=model,
            input=[sec_text]
        )
        emb = resp.data[0].embedding
        ids.append(sec_id)
        embeddings.append(emb)
        metadatas.append({"sec_id": sec_id})

    # Spin up an in-memory Chroma client
    client = chromadb.EphemeralClient()

    # Create (or recreate) the collection
    try:
        coll = client.get_collection("omd_sections")
        coll.delete(where={})
    except Exception:
        coll = client.create_collection(name="omd_sections")

    # Add the precomputed embeddings
    coll.add(
        ids=ids,
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
    Given a collection and a query string:
    1) Compute the query's OpenAI embedding
    2) Query the collection via `query_embeddings`
    3) Return section IDs whose distance ≥ threshold
    """
    # Ensure OpenAI key & same model
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # Compute embedding for the query
    resp = openai.embeddings.create(
        model=model,
        input=[query_text]
    )
    q_emb = resp.data[0].embedding

    # Perform vector search by embedding
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=max_results,
        include=["metadatas", "distances"]
    )

    # Unpack
    metas = results["metadatas"][0]
    dists = results["distances"][0]

    # Filter by threshold
    return [m["sec_id"] for m, dist in zip(metas, dists) if dist >= threshold]