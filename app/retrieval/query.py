import os, json
from pathlib import Path
import numpy as np
from app.utils.llm_client import embed, chat

INDEX_DIR = Path(os.getenv("RAG_INDEX_DIR", ".indices"))
K = int(os.getenv("RETRIEVE_K", "2"))

def cosine_topk(qvec: np.ndarray, m: np.ndarray, k: int):
  sims = (m @ qvec)  # assuming rows are normalized and qvec normalized
  idx = np.argsort(-sims)[:k]
  return [(int(i), float(sims[i])) for i in idx]

def retrieve(dept: str, query: str):
  dept = dept.lower()
  mpath = INDEX_DIR / dept / "embeddings.npy"
  meta = INDEX_DIR / dept / "meta.json"
  if not mpath.exists() or not meta.exists():
    return []
  m = np.load(mpath)
  q = embed(query)
  qv = np.array(q.data[0].embedding, dtype=np.float32)
  qv = qv / (np.linalg.norm(qv) + 1e-9)
  top = cosine_topk(qv, m, K)
  items = json.loads(meta.read_text())
  return [(items[i]["text"], s) for i, s in top]

def answer_from_context(query: str, ctx_texts):
  ctx = "\n\n".join([t for t,_ in ctx_texts])
  messages = [
    {"role":"system","content":"You are an ITSM assistant. Use the provided context to answer succinctly. If insufficient, say you don't know."},
    {"role":"user","content":f"Context:\n{ctx}\n\nQuestion: {query}"}
  ]
  res = chat(messages)
  return res.choices[0].message.content
