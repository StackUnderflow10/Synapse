
import re


class SectionParser:

    # Normalize common research-paper headings.
    KNOWN_HEADINGS = {
        "abstract": "abstract",
        "introduction": "introduction",
        "related work": "related_work",
        "background": "background",
        "method": "methods",
        "methods": "methods",
        "methodology": "methods",
        "model architecture": "model_architecture",
        "why self-attention": "why_self_attention",
        "experiments": "experiments",
        "experimental setup": "experimental_setup",
        "results": "results",
        "discussion": "discussion",
        "conclusion": "conclusion",
        "conclusions": "conclusion",
        "references": "references",
        "acknowledgements": "acknowledgements",
        "acknowledgments": "acknowledgements",
    }

    def detect_section(self, item):

        text = re.sub(
            r"\s+", " ", item["text"].strip()
        )

        normalized = text.lower()

        # Handle exact, unnumbered headings.
        if normalized in self.KNOWN_HEADINGS:
            return self.KNOWN_HEADINGS[normalized]

        # Handle numbered top-level headings:
        # 3 Model Architecture
        # 4 Why Self-Attention
        # 5 Training
        match = re.match(
            r"^\d+\s*[.]?\s+(.+)$",
            normalized
        )

        if match:

            title = match.group(1).strip()

            # Only accept short, likely heading lines.
            # Font size and boldness help avoid mistaking
            # ordinary numbered paragraphs for headings.
            is_heading_style = (
                item.get("bold", False)
                or item.get("font_size", 0) >= 11.5
            )

            if is_heading_style and len(title) <= 80:

                if title in self.KNOWN_HEADINGS:
                    return self.KNOWN_HEADINGS[title]

                # Preserve unknown heading names.
                return re.sub(
                    r"[^a-z0-9]+",
                    "_",
                    title
                ).strip("_")

        return None

    def organize(self, pages):

        sections = []
        current_section = "front_matter"

        for page in pages:

            for item in page["content"]:

                text = item["text"]

                detected = self.detect_section(item)

                if detected:
                    current_section = detected

                # Keep separate entries for each section/page.
                if (
                    not sections
                    or sections[-1]["section"] != current_section
                    or sections[-1]["page"] != page["page"]
                ):

                    sections.append({
                        "section": current_section,
                        "page": page["page"],
                        "content": ""
                    })

                # Don't include heading text in body content.
                if not detected:
                    sections[-1]["content"] += text + " "

        return sections
