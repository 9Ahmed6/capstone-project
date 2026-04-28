"""
Action-Based Video Understanding System — Streamlit entry point.

Week 1 scope:
    * Lay out the full UI surface (upload, action input, run button, results panes).
    * Load configuration and the action schema library.
    * Show a clean placeholder flow so weeks 2–7 can plug real pipeline modules in
      without restructuring the UI.

Run:
    streamlit run streamlit_app.py
"""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_ROOT / "configs" / "settings.yaml"
SCHEMA_PATH = PROJECT_ROOT / "schemas" / "action_library.json"


# ---------------------------------------------------------------------------
# Cached loaders
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_settings(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@st.cache_data(show_spinner=False)
def load_action_library(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dirs(settings: dict) -> None:
    """Make sure the directories referenced by settings.yaml exist."""
    for key in ("videos_dir", "samples_dir", "outputs_dir", "logs_dir"):
        Path(PROJECT_ROOT / settings["paths"][key]).mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Placeholder pipeline (weeks 2–6 will replace the body of these functions)
# ---------------------------------------------------------------------------
def placeholder_match_schema(action_text: str, library: dict) -> dict:
    """Naive substring match. Real embedding matcher arrives in Week 3."""
    text = action_text.strip().lower()
    if not text:
        return {"status": "empty", "matches": []}

    scored = []
    for entry in library.get("actions", []):
        haystack = " ".join(
            [entry["name"], entry["description"], *entry.get("aliases", [])]
        ).lower()
        if text in haystack or any(tok in haystack for tok in text.split()):
            scored.append({"id": entry["id"], "name": entry["name"], "score": 0.5})
    return {"status": "ok" if scored else "no_match", "matches": scored[:3]}


def placeholder_run_pipeline(video_path: Path, action_text: str) -> dict:
    """Stub: weeks 2–6 will replace this with real video/audio/pose/fusion calls."""
    return {
        "video": str(video_path.name),
        "query": action_text,
        "segments": [],
        "note": "Pipeline not yet implemented — Week 1 placeholder.",
    }


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
def main() -> None:
    settings = load_settings(CONFIG_PATH)
    library = load_action_library(SCHEMA_PATH)
    ensure_dirs(settings)

    st.set_page_config(
        page_title=settings["ui"]["page_title"],
        page_icon="🎬",
        layout="wide",
    )

    # ---- Sidebar -----------------------------------------------------------
    with st.sidebar:
        st.header("Project status")
        st.success("Week 1 — project skeleton ready.")
        st.caption(
            f"Schema library: **{len(library.get('actions', []))}** actions "
            f"(v{library.get('version', '?')})"
        )
        with st.expander("Effective settings", expanded=False):
            st.code(yaml.safe_dump(settings, sort_keys=False), language="yaml")

    # ---- Header ------------------------------------------------------------
    st.title("🎬 Action-Based Video Understanding")
    st.write(
        "Upload a video, describe the action you are looking for, and the system "
        "will return timestamped segments and exportable clips. The full multimodal "
        "pipeline is being built across an 8-week schedule — this Week 1 build "
        "covers the project skeleton and UI layout."
    )

    # ---- Inputs ------------------------------------------------------------
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("1. Upload a video")
        uploaded = st.file_uploader(
            "Video file",
            type=[ext.lstrip(".") for ext in settings["video"]["allowed_extensions"]],
            help=f"Max {settings['video']['max_upload_mb']} MB. "
                 f"Allowed: {', '.join(settings['video']['allowed_extensions'])}",
        )

    with col_right:
        st.subheader("2. Describe the action")
        action_text = st.text_input(
            "Action description",
            placeholder="e.g. 'person waving at the camera'",
        )

    run = st.button("Run analysis", type="primary", use_container_width=True)

    # ---- Run ---------------------------------------------------------------
    if run:
        if not uploaded:
            st.error("Please upload a video first.")
            return
        if not action_text.strip():
            st.error("Please enter an action description.")
            return

        # Save upload to data/videos so downstream modules can pick it up.
        videos_dir = PROJECT_ROOT / settings["paths"]["videos_dir"]
        target_path = videos_dir / uploaded.name
        with target_path.open("wb") as f:
            f.write(uploaded.getbuffer())

        with st.status("Running placeholder pipeline…", expanded=True) as status:
            st.write("Matching action against schema library…")
            match = placeholder_match_schema(action_text, library)
            st.write("Running video pipeline (stub)…")
            result = placeholder_run_pipeline(target_path, action_text)
            status.update(label="Done", state="complete")

        st.subheader("Schema match")
        st.json(match)

        st.subheader("Pipeline output")
        st.json(result)

        st.subheader("Video preview")
        st.video(str(target_path))

    # ---- Footer ------------------------------------------------------------
    st.divider()
    st.caption(
        f"{settings['project']['name']} v{settings['project']['version']} — "
        "Week 1 placeholder build."
    )


if __name__ == "__main__":
    main()
