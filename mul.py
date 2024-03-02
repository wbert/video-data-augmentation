import os
import cv2
import numpy as np
import random

def apply_random_multiply(frame):
    # Define random factors for multiplication
    factor_r = random.uniform(0.5, 2.0)
    factor_g = random.uniform(0.5, 2.0)
    factor_b = random.uniform(0.5, 2.0)
    
    # Multiply the frame by the random factors
    multiplied_frame = frame.astype(np.float32)
    multiplied_frame[:,:,0] *= factor_b
    multiplied_frame[:,:,1] *= factor_g
    multiplied_frame[:,:,2] *= factor_r
    
    # Clip pixel values to the valid range [0, 255]
    multiplied_frame = np.clip(multiplied_frame, 0, 255).astype(np.uint8)
    
    return multiplied_frame

def apply_random_multiply_to_video(video_path, output_path, num_frames=None):
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
            print(f"Warning: End of video '{video_path}' reached at frame {i + 1}.")
            break

        # Apply random multiply transformation
        multiplied_frame = apply_random_multiply(frame)

        # Check if multiplied frame has data
        if multiplied_frame is None:
            print(f"Warning: Skipping empty frame {i + 1} in video '{video_path}'.")
            continue

        # Write the transformed frame to the output video
        out.write(multiplied_frame)

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
            
            # Apply random multiply to the video
            apply_random_multiply_to_video(input_video_path, output_video_path)
            print(f"Random multiply applied to {filename}.")

if __name__ == "__main__":
    input_dir = "C:\\Users\\Wilbert\\Desktop\\data\\cleaned\\assault"
    output_dir = "C:\\Users\\Wilbert\\Desktop\\data\\augmented\\assaultmultiply"

    # Process all videos in the input directory
    process_videos_in_directory(input_dir, output_dir)

    print("All videos processed successfully.")
