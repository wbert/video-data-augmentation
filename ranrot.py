import os
import cv2
import numpy as np
import random

def apply_random_rotation(frame):
    # Define the rotation angle (random value between -30 and 30 degrees)
    angle = random.uniform(-30, 30)
    
    # Get the height and width of the frame
    height, width = frame.shape[:2]
    
    # Calculate the rotation center
    center = (width / 2, height / 2)
    
    # Perform the rotation
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_frame = cv2.warpAffine(frame, rotation_matrix, (width, height))
    
    return rotated_frame

def apply_random_rotation_to_video(video_path, output_path, num_frames=None):
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
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Check if the output video file was successfully created
    if not out.isOpened():
        print(f"Error: Could not create output video file '{output_path}'")
        return

    # Iterate over frames
    for i in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            break

        # Apply random rotation transformation
        rotated_frame = apply_random_rotation(frame)

        # Write the transformed frame to the output video
        out.write(rotated_frame)

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
            
            # Apply random rotation to the video
            apply_random_rotation_to_video(input_video_path, output_video_path)
            print(f"Random rotation applied to {filename}.")

if __name__ == "__main__":
    input_dir = "C:\\Users\\Wilbert\\Desktop\\data\\cleaned\\theft"
    output_dir = "C:\\Users\\Wilbert\\Desktop\\data\\augmented\\theftrot"

    # Process all videos in the input directory
    process_videos_in_directory(input_dir, output_dir)

    print("All videos processed successfully.")

