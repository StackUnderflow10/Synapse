import re

class SectionParser:

    SECTION_PATTERNS = {
        "abstract": r"^abstract$",
        "introduction": r"^\d*\.?\s*introduction$",
        "related_work": r"^\d*\.?\s*(related work|background)$",
        "methods": r"^\d*\.?\s*(method|methods|approach|model)$",
        "experiments": r"^\d*\.?\s*(experiments|experimental setup)$",
        "results": r"^\d*\.?\s*results$",
        "conclusion": r"^\d*\.?\s*conclusion(s)?$",
        "references": r"^references$",
    }

    def detect_section(self, text):

        normalized = text.strip().lower()

        for section, pattern in self.SECTION_PATTERNS.items():

            if re.match(pattern, normalized):
                return section

        return None

    def organize(self, pages):

        sections = []
        current_section = "unknown"

        for page in pages:

            for item in page["content"]:

                text = item["text"]

                detected = self.detect_section(text)

                if detected:
                    current_section = detected

                    sections.append({
                        "section": current_section,
                        "page": page["page"],
                        "content": ""
                    })

                else:

                    if not sections:
                        sections.append({
                            "section": current_section,
                            "page": page["page"],
                            "content": ""
                        })

                    sections[-1]["content"] += text + " "

        return sections