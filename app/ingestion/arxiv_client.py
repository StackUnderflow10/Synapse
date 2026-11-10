import arxiv
import re

from pathlib import Path

from app.config import PAPERS_DIR

class ArxivClient:

    def __init__(self):
        self.client = arxiv.Client()

    def extract_paper_id(self, value: str) -> str:
        """
        Accept:
        - 1706.03762
        - https://arxiv.org/abs/1706.03762
        - https://arxiv.org/pdf/1706.03762
        """

        value = value.strip()

        match = re.search(
            r"(\d{4}\.\d{4,5})(?:v\d+)?",
            value
        )

        if not match:
            raise ValueError("Invalid arXiv ID or URL")

        return match.group(1)

    def fetch_paper(self, paper_id: str):

        search = arxiv.Search(
            id_list=[paper_id]
        )

        results = list(self.client.results(search))

        if not results:
            raise ValueError("Paper not found")

        return results[0]

    def download_paper(self, paper_id: str):

        paper = self.fetch_paper(paper_id)

        output_path = PAPERS_DIR / f"{paper_id}.pdf"

        paper.download_pdf(
            filename=str(output_path)
        )

        return {
            "id": paper_id,
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "abstract": paper.summary,
            "published": paper.published.isoformat(),
            "pdf_path": str(output_path),
            "arxiv_url": paper.entry_id
        }

if __name__ == "__main__":

    client = ArxivClient()

    paper = client.download_paper("1706.03762")

    print(paper)