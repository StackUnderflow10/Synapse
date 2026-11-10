from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = ROOT_DIR / "data"
PAPERS_DIR = DATA_DIR / "papers"
PARSED_DIR = DATA_DIR / "parsed"
CHROMA_DIR = DATA_DIR / "chroma_db"

# Create directories if they don't exist
for directory in [PAPERS_DIR, PARSED_DIR, CHROMA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Embedding model
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# Retrieval configuration
TOP_K = 5

# Chunking configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 75