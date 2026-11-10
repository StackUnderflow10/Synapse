from app.ingestion.pdf_parser import PDFParser
from app.ingestion.section_parser import SectionParser

pdf_path = "data/papers/1706.03762.pdf"

parser = PDFParser()
section_parser = SectionParser()

pages = parser.parse(pdf_path)

sections = section_parser.organize(pages)

for section in sections:

    print("\nSECTION:", section["section"])
    print("PAGE:", section["page"])
    print("CONTENT:", section["content"][:300])