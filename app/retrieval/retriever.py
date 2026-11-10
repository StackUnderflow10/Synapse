from app.retrieval.vector_store import PaperVectorStore

class PaperRetriever:

    def __init__(self):

        self.store = PaperVectorStore()

    def retrieve(self, query, top_k=5):

        results = self.store.search(query, top_k)

        passages = []

        for i in range(len(results["ids"][0])):

            passages.append({

                "text": results["documents"][0][i],

                "metadata": results["metadatas"][0][i],

                "distance": results["distances"][0][i]

            })

        return passages