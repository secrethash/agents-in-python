import chromadb
from sentence_transformers import SentenceTransformer

SIMILARITY_THRESHOLD = 0.85  # 0 = completely different (lenient), 1 = identical (stricter)

# Load a lightweight local embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB - stores data in a local folder called 'memory_db'
client = chromadb.PersistentClient(path="./memory_db")
collection = client.get_or_create_collection("agent_memory")

def save_memory(text: str) -> str:
    """Save a piece of information to a long-term memory, skipping if a similar memory already exists."""
    embedding = embedder.encode(text).tolist()

    # if memory isn't empty check for deduplication first
    if collection.count() > 0:
        results =collection.query(
            query_embeddings=[embedding],
            n_results=1
        )
        top_distance = results["distances"][0][0]
        # ChromaDB return L2 distance - lower means more similar
        # Convert to a 0-1 similarity score
        similarity = 1 / (1 + top_distance)
        
        if similarity >= SIMILARITY_THRESHOLD:
            existing = results["documents"][0][0]
            return f"Already in memory: '{existing}' - skipped."

    # No duplicates found, save it
    existing_count = collection.count()
    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[f"mem_{existing_count + 1}"]
    )

    return f"Saved to memory: '{text}'"

def search_memory(query: str, n_results: int = 3) -> str:
    """Search long-term memory for relevant information."""

    if collection.count() == 0:
        return "Memory is empty."
    
    embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=min(n_results, collection.count())
    )

    memories = results["documents"][0]
    if not memories:
        return "No relevant memories found."
    
    return "Relevant memories:\n" + "\n".join(f"- {m}" for m in memories)