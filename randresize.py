import os
import cv2
import numpy as np
import random

def apply_random_resize(frame):
    # Define random scale factors for resizing
    scale_x = random.uniform(0.5, 2.0)
    scale_y = random.uniform(0.5, 2.0)
    
    # Resize the frame using the scale factors
    resized_frame = cv2.resize(frame, None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_LINEAR)
    
    return resized_frame

def apply_random_resize_to_video(video_path, output_path, num_frames=None):
    # Open video file
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video file was successfully opened
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_path}'")
        return
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    num_frames_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Determine the number of frames to process
    if num_frames is None:
        num_frames = num_frames_total

    # Create output video

    
# Create output video
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))

    
    # Check if the output video file was successfully created
    if not out.isOpened():
        print(f"Error: Could not create output video file '{output_path}'")
        return

    # Iterate over frames
    for i in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            print(f"Warning: End of video '{video_path}' reached at frame {i + 1}.")
            break

        # Apply random resize transformation
        resized_frame = apply_random_resize(frame)

        # Check if resized frame has data
        if resized_frame is None:
            print(f"Warning: Skipping empty frame {i + 1} in video '{video_path}'.")
            continue

        # Write the transformed frame to the output video
        out.write(resized_frame)

        # Print progress
        print(f"Processed frame {i + 1}/{num_frames_total} for video {video_path}")

    # Release video capture and writer
    cap.release()
    out.release()

def process_videos_in_directory(input_dir, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith((".mp4",".mov")):  # Adjust this condition based on your file types
            input_video_path = os.path.join(input_dir, filename)
            output_video_path = os.path.join(output_dir, filename)
            
            # Apply random resize to the video
            apply_random_resize_to_video(input_video_path, output_video_path)
            print(f"Random resize applied to {filename}.")

if __name__ == "__main__":
    input_dir = "C:\\Users\\Wilbert\\Desktop\\data\\cleaned\\theft"
    output_dir = "C:\\Users\\Wilbert\\Desktop\\data\\augmented\\theftresize"

    # Process all videos in the input directory
    process_videos_in_directory(input_dir, output_dir)

    print("All videos processed successfully.")

