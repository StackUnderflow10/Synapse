from app.config import CHUNK_SIZE, CHUNK_OVERLAP

class PaperChunker:

    def chunk_text(self, text):

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):

            end = min(start + CHUNK_SIZE, len(words))

            chunk = " ".join(words[start:end])

            chunks.append(chunk)

            if end == len(words):
                break

            start = end - CHUNK_OVERLAP

        return chunks

    
    def create_chunks(self, paper_id, sections):

        all_chunks = []

        # Global counter ensures unique IDs across the paper
        global_chunk_index = 0

        for section in sections:

            text = section["content"]

            chunks = self.chunk_text(text)

            for local_index, chunk in enumerate(chunks):

                all_chunks.append({

                    # Globally unique chunk identifier
                    "chunk_id": (
                        f"{paper_id}_chunk_{global_chunk_index}"
                    ),

                    "paper_id": paper_id,

                    "section": section["section"],

                    "page": section["page"],

                    # Position within the individual section entry
                    "chunk_index": local_index,

                    "text": chunk

                })

                global_chunk_index += 1

        return all_chunks
