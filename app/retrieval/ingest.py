import os, json, sys
from pathlib import Path
import numpy as np
from app.utils.llm_client import embed

INDEX_DIR = Path(os.getenv("RAG_INDEX_DIR", ".indices"))

def read_texts(paths):
  docs=[]
  for p in paths:
    pth=Path(p)
    if pth.is_dir():
      for f in pth.rglob("*"):
        if f.suffix.lower() in {".md",".txt"}:
          docs.append((str(f), f.read_text(encoding="utf-8", errors="ignore")))
    elif pth.is_file():
      docs.append((str(pth), pth.read_text(encoding="utf-8", errors="ignore")))
  return docs

def normalize(vecs: np.ndarray):
  n = np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-9
  return vecs / n

def main():
  if len(sys.argv) < 2:
    print("Usage: python -m app.retrieval.ingest <dept_dir> [<dept_dir> ...]")
    sys.exit(1)
  INDEX_DIR.mkdir(parents=True, exist_ok=True)
  for dept_dir in sys.argv[1:]:
    dept = Path(dept_dir).name.lower()
    docs = read_texts([dept_dir])
    if not docs:
      print(f"No docs in {dept_dir}")
      continue
    texts = [t for _, t in docs]
    emb = embed(texts)
    vecs = np.array([emb.data[0].embedding]*(len(texts)), dtype=np.float32) if len(emb.data)==1 else np.array([d.embedding for d in emb.data], dtype=np.float32)
    vecs = normalize(vecs)
    out_dir = INDEX_DIR / dept
    out_dir.mkdir(parents=True, exist_ok=True)
    np.save(out_dir/"embeddings.npy", vecs)
    with open(out_dir/"meta.json", "w", encoding="utf-8") as f:
      json.dump([{"path": docs[i][0], "text": texts[i]} for i in range(len(texts))], f)
    print(f"Indexed {len(texts)} docs for {dept} -> {out_dir}")

if __name__ == "__main__":
  main()
