from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Load model once (cached)
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# Convert schema entry into searchable text
def build_text(entry):

    motion = entry.get("motion", {})
    motion_text = " ".join([
        motion.get("pattern", ""),
        motion.get("direction", "")
    ])

    body = " ".join(entry.get("body_parts", []))
    objects = " ".join(entry.get("objects", []))

    return " ".join([
        entry["name"],
        entry["description"],
        " ".join(entry.get("aliases", [])),
        motion_text,
        body,
        objects
    ])


# MAIN MATCH FUNCTION
def match_action(action_text, library, threshold=0.5):

    if not action_text.strip():
        return {"status": "empty"}

    texts = [build_text(a) for a in library["actions"]]
    print("QUERY:", action_text)

    for i, entry in enumerate(library["actions"]):
        print(f"SCHEMA {i}:", build_text(entry))

    # Encode
    query_vec = model.encode([action_text])
    schema_vecs = model.encode(texts)

    # Compute similarity
    scores = cosine_similarity(query_vec, schema_vecs)[0]
    print("SCORES:", scores)

    # Best match
    best_idx = scores.argmax()
    best_score = float(scores[best_idx])
    best_action = library["actions"][best_idx]

    # Match decision
    if best_score >= threshold:
        return {
            "status": "matched",
            "best_match": {
                "id": best_action["id"],
                "name": best_action["name"],
                "score": round(best_score, 4)
            }
        }

    # Otherwise create draft
    return {
        "status": "new_schema_draft",
        "draft": {
            "name": action_text
        }
    }
