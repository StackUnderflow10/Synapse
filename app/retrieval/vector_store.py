import chromadb

from app.config import CHROMA_DIR, TOP_K

from app.retrieval.embeddings import EmbeddingService

class PaperVectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DIR)
        )

        self.collection = self.client.get_or_create_collection(
            name="research_papers"
        )

        self.embedding_service = EmbeddingService()

    def add_chunks(self, chunks):

        if not chunks:
            return

        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.embedding_service.embed_documents(
            texts
        )

        self.collection.upsert(

            ids=[chunk["chunk_id"] for chunk in chunks],

            embeddings=embeddings,

            documents=texts,

            metadatas=[
                {
                    "paper_id": chunk["paper_id"],
                    "section": chunk["section"],
                    "page": chunk["page"],
                    "chunk_index": chunk["chunk_index"]
                }
                for chunk in chunks
            ]
        )

    def search(self, query, top_k=TOP_K):

        query_embedding = self.embedding_service.embed_query(
            query
        )

        results = self.collection.query(

            query_embeddings=[query_embedding],

            n_results=top_k

        )

        return results