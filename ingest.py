"""
Кітапты жүктеп, чанктарға бөліп, эмбеддинг жасайды және vectorstore-ге сақтайды.
Қолдану: python ingest.py <файл_жолы>
"""

import os
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import numpy as np
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
STORE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db")


def load_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return _load_pdf(file_path)
    elif ext in (".txt", ".md"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError(f"Қолдауы жоқ формат: {ext}. PDF, TXT немесе MD файл беріңіз.")


def _load_pdf(file_path: str) -> str:
    try:
        import PyPDF2
        text = []
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            total = len(reader.pages)
            for i, page in enumerate(reader.pages):
                content = page.extract_text() or ""
                text.append(content)
                if (i + 1) % 50 == 0:
                    print(f"  {i+1}/{total} бет оқылды...")
        return "\n".join(text)
    except ImportError:
        raise ImportError("PyPDF2 орнатылмаған.")


def split_into_chunks(text: str) -> list[str]:
    enc = tiktoken.get_encoding("cl100k_base")
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    tokens = enc.encode(text)
    total_tokens = len(tokens)
    chunks = []
    start = 0
    while start < total_tokens:
        end = min(start + CHUNK_SIZE, total_tokens)
        chunk_text = enc.decode(tokens[start:end]).strip()
        if chunk_text:
            chunks.append(chunk_text)
        if end >= total_tokens:
            break
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def get_embeddings(texts: list[str], batch_size: int = 100) -> list[list[float]]:
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        print(f"  Эмбеддинг: {i+len(batch)}/{len(texts)} чанк...")
        response = client.embeddings.create(model=EMBED_MODEL, input=batch)
        all_embeddings.extend([item.embedding for item in response.data])
    return all_embeddings


def save_store(chunks: list[str], embeddings: list[list[float]], source: str, collection: str):
    os.makedirs(STORE_DIR, exist_ok=True)
    emb_array = np.array(embeddings, dtype=np.float32)
    np.save(os.path.join(STORE_DIR, f"{collection}.npy"), emb_array)
    meta = {
        "source": source,
        "embed_model": EMBED_MODEL,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "chunks": chunks,
    }
    with open(os.path.join(STORE_DIR, f"{collection}.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def ingest(file_path: str, collection_name: str = "book"):
    print(f"\n Файл жүктелуде: {file_path}")
    text = load_text(file_path)
    print(f" Жалпы мәтін: {len(text):,} таңба")

    print(f"\n Чанктарға бөлу (чанк={CHUNK_SIZE} токен, қабаттасу={CHUNK_OVERLAP})...")
    chunks = split_into_chunks(text)
    print(f" {len(chunks)} чанк жасалды")

    print(f"\n Эмбеддингтер жасалуда (модель: {EMBED_MODEL})...")
    embeddings = get_embeddings(chunks)

    print(f"\n Сақталуда: {STORE_DIR}")
    save_store(chunks, embeddings, os.path.basename(file_path), collection_name)

    print(f"\n Дайын! {len(chunks)} чанк '{collection_name}' коллекциясына сақталды.\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Қолдану: python ingest.py <файл.pdf немесе файл.txt>")
        sys.exit(1)

    file_path = sys.argv[1]
    collection = sys.argv[2] if len(sys.argv) > 2 else "book"

    if not os.path.exists(file_path):
        print(f"Қате: файл табылмады: {file_path}")
        sys.exit(1)

    ingest(file_path, collection)
