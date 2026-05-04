from __future__ import annotations

import cv2
import mediapipe as mp
import csv
import os
from pathlib import Path


# ---------------------------------------------------
# Draw landmarks on frame
# ---------------------------------------------------
def draw_landmarks(frame, results, mp_holistic, mp_drawing):

    if results.face_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS
        )

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS
        )

    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS
        )

    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS
        )


# ---------------------------------------------------
# MAIN PIPELINE FUNCTION (IMPORTANT)
# ---------------------------------------------------
def run_pose_pipeline(video_path: str, output_dir: str) -> dict:

    video_path = Path(video_path)
    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    output_csv = output_dir / f"{video_path.stem}_landmarks.csv"
    output_video = output_dir / f"{video_path.stem}_annotated.mp4"

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = cv2.VideoWriter(
        str(output_video),
        cv2.VideoWriter_fourcc(*"avc1"),
        fps if fps > 0 else 30,
        (width, height)
    )

    mp_holistic = mp.solutions.holistic
    mp_drawing = mp.solutions.drawing_utils

    rows = []

    with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as holistic:

        frame_idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(rgb)

            # Draw landmarks
            draw_landmarks(frame, results, mp_holistic, mp_drawing)

            # Save pose landmarks
            if results.pose_landmarks:
                for i, lm in enumerate(results.pose_landmarks.landmark):
                    rows.append([frame_idx, "pose", i, lm.x, lm.y, lm.z, lm.visibility])

            # Face
            if results.face_landmarks:
                for i, lm in enumerate(results.face_landmarks.landmark):
                    rows.append([frame_idx, "face", i, lm.x, lm.y, lm.z, None])

            # Left hand
            if results.left_hand_landmarks:
                for i, lm in enumerate(results.left_hand_landmarks.landmark):
                    rows.append([frame_idx, "left_hand", i, lm.x, lm.y, lm.z, None])

            # Right hand
            if results.right_hand_landmarks:
                for i, lm in enumerate(results.right_hand_landmarks.landmark):
                    rows.append([frame_idx, "right_hand", i, lm.x, lm.y, lm.z, None])

            writer.write(frame)

            frame_idx += 1

    cap.release()
    writer.release()

    # Save CSV
    with open(output_csv, "w", newline="") as f:
        writer_csv = csv.writer(f)
        writer_csv.writerow(["frame", "part", "id", "x", "y", "z", "visibility"])
        writer_csv.writerows(rows)

    return {
        "csv": str(output_csv),
        "video": str(output_video),
        "frames_processed": frame_idx
    }