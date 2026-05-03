import os
import jsonlines
import numpy as np
import faiss
import time
from sentence_transformers import SentenceTransformer

# ==============================
# PATHS (EDIT IF NEEDED)
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "..", "data")
INDEX_DIR = os.path.join(BASE_DIR, "..", "faiss_index")

os.makedirs(INDEX_DIR, exist_ok=True)

INPUT_FILE = os.path.join(DATA_DIR, "all_chunks.jsonl")

INDEX_FILE = os.path.join(INDEX_DIR, "faiss.index")
META_FILE = os.path.join(INDEX_DIR, "metadata.jsonl")
CHECKPOINT_FILE = os.path.join(INDEX_DIR, "checkpoint.txt")

# ==============================
# CONFIG
# ==============================
BATCH_SIZE = 256
N_LIST = 256
N_PROBE = 15
LOG_INTERVAL = 5000

# ==============================
# MODEL
# ==============================
print("🔹 Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# ==============================
# STEP 1: TRAIN IVF (sample)
# ==============================
print("\n🔹 Sampling for IVF training...")

sample_texts = []

with jsonlines.open(INPUT_FILE) as reader:
    for i, obj in enumerate(reader):
        sample_texts.append(obj["text"])
        if len(sample_texts) >= 50000:
            break

print(f"Sample size: {len(sample_texts)}")

sample_emb = model.encode(sample_texts, batch_size=128)
sample_emb = np.array(sample_emb).astype("float32")

faiss.normalize_L2(sample_emb)

dim = sample_emb.shape[1]

quantizer = faiss.IndexFlatIP(dim)
index = faiss.IndexIVFFlat(
    quantizer,
    dim,
    N_LIST,
    faiss.METRIC_INNER_PRODUCT
)

print("🔹 Training index...")
index.train(sample_emb)

# ==============================
# STEP 2: LOAD CHECKPOINT
# ==============================
start_index = 0

if os.path.exists(CHECKPOINT_FILE):
    with open(CHECKPOINT_FILE, "r") as f:
        start_index = int(f.read().strip())
    print(f"🔁 Resuming from: {start_index}")
else:
    print("Starting fresh...")

# ==============================
# STEP 3: STREAM + EMBED
# ==============================
print("\n🔹 Embedding + indexing...")

batch_texts = []
batch_meta = []
total = 0
processed = 0

start_time = time.time()

meta_writer = jsonlines.open(META_FILE, "a")

def save_checkpoint(count):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(count))

with jsonlines.open(INPUT_FILE) as reader:

    for idx, obj in enumerate(reader):

        if idx < start_index:
            continue

        batch_texts.append(obj["text"])
        batch_meta.append({
            "ticket_id": obj["ticket_id"],
            "timestamp": obj["timestamp"]
        })

        if len(batch_texts) == BATCH_SIZE:

            emb = model.encode(
                batch_texts,
                batch_size=BATCH_SIZE,
                convert_to_numpy=True,
                normalize_embeddings=True
            )

            emb = np.array(emb).astype("float32")
            index.add(emb)

            for m in batch_meta:
                meta_writer.write(m)

            total += len(batch_texts)
            processed = idx

            # ==============================
            # LOGGING
            # ==============================
            if total % LOG_INTERVAL == 0:
                elapsed = time.time() - start_time
                speed = total / elapsed
                print(f"✅ Indexed: {total} | Speed: {speed:.2f} chunks/sec")

                save_checkpoint(processed)

            batch_texts = []
            batch_meta = []

# ==============================
# HANDLE REMAINING
# ==============================
if batch_texts:
    emb = model.encode(
        batch_texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    emb = np.array(emb).astype("float32")
    index.add(emb)

    for m in batch_meta:
        meta_writer.write(m)

meta_writer.close()

# ==============================
# FINAL SAVE
# ==============================
index.nprobe = N_PROBE

print("\n🔹 Saving index...")
faiss.write_index(index, INDEX_FILE)

save_checkpoint(processed)

print(f"\n🚀 DONE! Total indexed: {total}")