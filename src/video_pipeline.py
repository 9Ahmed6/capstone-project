from __future__ import annotations
import cv2 # for video processing
import os # for file/folder operations
import json # for saving metadata as json

# This function reads a video file and returns key technical details
# like FPS, frame count, resolution, and duration
def extract_video_metadata(video_path):
    #open the video file
    cap = cv2.VideoCapture(video_path)

    #check if the file is opened correctly
    if not cap.isOpened():
        raise ValueError("Error opening video file")
    
    #frames per second
    fps = cap.get(cv2.CAP_PROP_FPS)

    #total number of frames
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    #width and height
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    #duration = total frames / fps
    duration = frame_count / fps if fps > 0 else 0

    #store all metadata in a dictionary
    metadata = {
        "video_path": video_path,
        "fps": fps,
        "frame_count": frame_count,
        "resolution": f"{width}x{height}",
        "duration": duration
    }

    #release video resource
    cap.release()

    return metadata

# this function saves extracted metadata so later modules
# can use it without reprocessing the video
def save_metadata(metadata, output_path):
    #open file in write mode
    with open(output_path, "w") as f:
        #save nicely formatted JSON
        json.dump(metadata, f, indent=4)

#this function saves one frame every x seconds
#sample interval default is 1 so means 1 frame every 1 second
def extract_frames(videopath, output_folder, sample_interval=1):
    
    #create output folder if missing
    os.makedirs(output_folder, exist_ok=True)

    #open video
    cap = cv2.VideoCapture(videopath)

    #check if video is loaded
    if not cap.isOpened():
        raise ValueError("Cannot open video")
    
    #fps helps calculate frame intervals
    fps = cap.get(cv2.CAP_PROP_FPS)

    #track frame position
    frame_idx = 0

    #track saved frame count
    saved_count = 0

    #read frame by frame
    while True:

        #ret = success/fail, frame is the image
        ret, frame = cap.read()

        #stop when video ends
        if not ret:
            break
        
        #save frame every sample interval seconds
        if frame_idx % int(fps * sample_interval) == 0:
            #example: frame_00001.jpg
            frame_name = os.path.join(
                output_folder,
                f"frame_{saved_count:05d}.jpg"
            )
            #save image
            cv2.imwrite(frame_name, frame)
            #increase saved count
            saved_count += 1
        #move to next frame
        frame_idx += 1
    #release memory
    cap.release()

    return saved_count