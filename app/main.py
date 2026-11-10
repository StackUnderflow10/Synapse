import gradio as gr

from scripts.ingest_paper import ingest

from app.retrieval.retriever import PaperRetriever

retriever = PaperRetriever()

def add_paper(paper_id):

    try:

        ingest(paper_id)

        return f"Successfully ingested paper: {paper_id}"

    except Exception as error:

        return f"Error: {str(error)}"

def search_paper(question):

    results = retriever.retrieve(question)

    output = []

    for result in results:

        metadata = result["metadata"]

        output.append(
            f"""
            ### {metadata['paper_id']}

            **Section:** {metadata['section']}

            **Page:** {metadata['page']}

            {result['text']}

            ---
            """
        )

    return "\n".join(output)

with gr.Blocks(title="Research Paper Copilot") as demo:

    gr.Markdown(
        """
        # Research Paper Copilot

        Your AI-powered research assistant.

        Ingest research papers, retrieve evidence
        and explore scientific literature.
        """
    )

    with gr.Tab("Ingest Paper"):

        paper_id = gr.Textbox(
            label="arXiv ID or URL",
            placeholder="1706.03762"
        )

        ingest_button = gr.Button("Ingest Paper")

        ingest_status = gr.Textbox(
            label="Status"
        )

        ingest_button.click(
            add_paper,
            inputs=paper_id,
            outputs=ingest_status
        )

    with gr.Tab("Search Papers"):

        question = gr.Textbox(
            label="Research question",
            placeholder="Explain the self-attention mechanism"
        )

        search_button = gr.Button("Search Evidence")

        search_output = gr.Markdown()

        search_button.click(
            search_paper,
            inputs=question,
            outputs=search_output
        )

if __name__ == "__main__":

    demo.launch()