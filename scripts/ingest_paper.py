import sys

from app.ingestion.arxiv_client import ArxivClient
from app.ingestion.pdf_parser import PDFParser
from app.ingestion.section_parser import SectionParser
from app.ingestion.chunker import PaperChunker

from app.retrieval.vector_store import PaperVectorStore

def ingest(paper_id):

    # 1. Download paper
    client = ArxivClient()

    paper = client.download_paper(paper_id)

    print("Downloaded:", paper["title"])

    # 2. Extract PDF text
    parser = PDFParser()

    pages = parser.parse(paper["pdf_path"])

    # 3. Detect sections
    section_parser = SectionParser()

    sections = section_parser.organize(pages)

    # 4. Generate chunks
    chunker = PaperChunker()

    chunks = chunker.create_chunks(
        paper_id,
        sections
    )

    # 5. Index chunks
    store = PaperVectorStore()

    store.add_chunks(chunks)

    print("Ingestion complete!")

    print("Total pages:", len(pages))

    print("Total sections:", len(sections))

    print("Total chunks:", len(chunks))

if __name__ == "__main__":

    paper_id = sys.argv[1]

    ingest(paper_id)