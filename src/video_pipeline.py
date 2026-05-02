import cv2
import mediapipe as mp
import csv
import os

def draw_landmarks(frame, results, mp_holistic, mp_drawing):
    # Draw face landmarks if MediaPipe detected a face.
    if results.face_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS
        )

    # Draw body pose landmarks so we can visualize body movement.
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS
        )

    # Draw left hand landmarks when the left hand is visible.
    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS
        )

    # Draw right hand landmarks when the right hand is visible.
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS
        )

def main():
    # Input video file that will be processed frame by frame.
    video_path = "samples/test.mp4"

    # Output files for saving landmark data and annotated video.
    output_csv = "outputs/holistic_landmarks.csv"
    output_video = "outputs/holistic_annotated.mp4"

    # Create the outputs folder if it does not already exist.
    os.makedirs("outputs", exist_ok=True)

    # Open the video file.
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Could not open video:", video_path)
        return

    # Read basic video properties so the saved video matches the input.
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # VideoWriter saves the processed frames into a new video file.
    writer = cv2.VideoWriter(
        output_video,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps if fps > 0 else 30,
        (width, height)
    )

    mp_holistic = mp.solutions.holistic
    mp_drawing = mp.solutions.drawing_utils
    rows = []

    # Holistic detects pose, face, and hands in one pipeline.
    with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as holistic:
        frame_idx = 0

        while True:
            # Read one frame from the video.
            ret, frame = cap.read()
            if not ret:
                break

            # MediaPipe expects RGB, but OpenCV reads BGR.
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(rgb)

            # Draw detected landmarks on the current frame.
            draw_landmarks(frame, results, mp_holistic, mp_drawing)

            # Save pose landmarks for later analysis or machine learning.
            if results.pose_landmarks:
                for landmark_id, lm in enumerate(results.pose_landmarks.landmark):
                    rows.append([frame_idx, "pose", landmark_id, lm.x, lm.y, lm.z, lm.visibility])

            # Save face landmarks if they are detected.
            if results.face_landmarks:
                for landmark_id, lm in enumerate(results.face_landmarks.landmark):
                    rows.append([frame_idx, "face", landmark_id, lm.x, lm.y, lm.z, None])

            # Save left hand landmarks if they are detected.
            if results.left_hand_landmarks:
                for landmark_id, lm in enumerate(results.left_hand_landmarks.landmark):
                    rows.append([frame_idx, "left_hand", landmark_id, lm.x, lm.y, lm.z, None])

            # Save right hand landmarks if they are detected.
            if results.right_hand_landmarks:
                for landmark_id, lm in enumerate(results.right_hand_landmarks.landmark):
                    rows.append([frame_idx, "right_hand", landmark_id, lm.x, lm.y, lm.z, None])

            # Write the processed frame into the output video.
            writer.write(frame)

            # Show the processed video on screen for live checking.
            cv2.imshow("Video", frame)

            # Press q to stop the video early.
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            frame_idx += 1

    # Release resources after processing finishes.
    cap.release()
    writer.release()
    cv2.destroyAllWindows()

    # Save all landmark data into a CSV file.
    with open(output_csv, "w", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["frame", "part", "landmark_id", "x", "y", "z", "visibility"])
        csv_writer.writerows(rows)

    print("Saved landmarks to:", output_csv)
    print("Saved annotated video to:", output_video)

if __name__ == "__main__":
    main()