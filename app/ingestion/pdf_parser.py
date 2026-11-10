import pymupdf

class PDFParser:

    def parse(self, pdf_path):

        document = pymupdf.open(pdf_path)

        pages = []

        for page_number, page in enumerate(document, start=1):

            blocks = page.get_text("dict")["blocks"]

            page_text = []

            for block in blocks:

                if "lines" not in block:
                    continue

                for line in block["lines"]:

                    for span in line["spans"]:

                        text = span["text"].strip()

                        if not text:
                            continue

                        page_text.append({
                            "text": text,
                            "font_size": span["size"],
                            "bold": bool(span["flags"] & 16),
                        })

            pages.append({
                "page": page_number,
                "content": page_text
            })

        return pages