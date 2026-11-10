from app.retrieval.retriever import PaperRetriever

retriever = PaperRetriever()

query = "Why is self-attention better than recurrent networks?"

results = retriever.retrieve(query)

for result in results:

    metadata = result["metadata"]

    print("\n------------------------")

    print("SECTION:", metadata["section"])

    print("PAGE:", metadata["page"])

    print("DISTANCE:", result["distance"])

    print("TEXT:", result["text"][:500])