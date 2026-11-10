from app.retrieval.retriever import PaperRetriever

from app.generation.llm import LLMService

from app.generation.prompts import QA_SYSTEM_PROMPT

class ResearchQA:

    def __init__(self):

        self.retriever = PaperRetriever()

        self.llm = LLMService()

    def answer(self, question):

        passages = self.retriever.retrieve(
            question,
            top_k=5
        )

        if not passages:

            return {
                "answer": "No relevant evidence found.",
                "citations": []
            }

        evidence = ""

        citations = []

        for index, passage in enumerate(passages):

            metadata = passage["metadata"]

            evidence += f"""
            Evidence {index + 1}:

            Paper: {metadata['paper_id']}
            Section: {metadata['section']}
            Page: {metadata['page']}

            Text:
            {passage['text']}
            """

            citations.append({
                "paper_id": metadata["paper_id"],
                "section": metadata["section"],
                "page": metadata["page"]
            })

        user_prompt = f"""
        QUESTION:
        {question}

        AVAILABLE EVIDENCE:
        {evidence}

        Answer using only this evidence.
        """

        answer = self.llm.generate(
            QA_SYSTEM_PROMPT,
            user_prompt
        )

        return {
            "answer": answer,
            "citations": citations
        }