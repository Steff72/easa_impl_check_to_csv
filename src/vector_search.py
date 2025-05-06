import os
import chromadb
from chromadb import PersistentClient
from openai import OpenAI

# OpenAI v1-Client initialisieren
_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def init_chroma(sections: dict[str, str]) -> chromadb.api.models.Collection:
    """
    Lädt oder erzeugt eine persistent gespeicherte Chroma-Collection.
    Beim ersten Lauf werden alle Sektionen embeddet und gespeichert,
    danach wird die bestehende DB geladen.
    """
    model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    persist_dir = os.getenv("CHROMA_PERSIST_DIR", ".chromadb")

    client = PersistentClient(path=persist_dir)
    try:
        return client.get_collection("omd_sections")
    except chromadb.errors.NotFoundError:
        coll = client.create_collection(name="omd_sections")

        ids, docs, embs, metas = [], [], [], []
        for sec_id, sec_text in sections.items():
            # nur ein einziger String statt [sec_text]
            resp = _ai.embeddings.create(
                model=model,
                input=sec_text
            )
            emb = resp.data[0].embedding

            ids.append(sec_id)
            docs.append(sec_text)
            embs.append(emb)
            metas.append({"sec_id": sec_id})

        coll.add(
            ids=ids,
            embeddings=embs,
            documents=docs,
            metadatas=metas
        )
        return coll

def search_candidates(
    collection: chromadb.api.models.Collection,
    query_text: str,
    threshold: float,
    max_results: int
) -> list[str]:
    """
    Erstellt das Query-Embedding als einzelner String und führt
    die Vektor-Suche in Chroma durch.
    Liefert nur IDs, deren Abstand >= threshold.
    """
    model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # nur ein einziger String statt [query_text]
    resp = _ai.embeddings.create(
        model=model,
        input=query_text
    )
    q_emb = resp.data[0].embedding

    results = collection.query(
        query_embeddings=[q_emb],
        n_results=max_results,
        include=["metadatas", "distances"]
    )
    metas = results["metadatas"][0]
    dists = results["distances"][0]

    return [
        m["sec_id"]
        for m, dist in zip(metas, dists)
        if dist >= threshold
    ]