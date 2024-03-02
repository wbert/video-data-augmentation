
import os
import cv2
import numpy as np
import random

def apply_static_shear_effect(frame, shear_factor):
    """
    Apply static shear effect to the frame.
    
    Parameters:
        frame (numpy.ndarray): The input frame.
        shear_factor (float): The shear factor to apply.
    
    Returns:
        numpy.ndarray: The frame with static shear effect applied.
    """
    # Define the transformation matrix
    M = np.array([[1, shear_factor, 0], [0, 1, 0]])
    
    # Apply the transformation
    sheared_frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))
    
    return sheared_frame

def apply_static_shear_effect_to_video(video_path, output_path, shear_factor):
    """
    Apply static shear effect to each frame of the input video and save the result to a new video.
    
    Parameters:
        video_path (str): The path to the input video file.
        output_path (str): The path to save the output video file.
        shear_factor (float): The shear factor to apply.
    """
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

    # Create output video
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Check if the output video file was successfully created
    if not out.isOpened():
        print(f"Error: Could not create output video file '{output_path}'")
        return

    # Iterate over frames
    for i in range(num_frames_total):
        ret, frame = cap.read()
        if not ret:
            print(f"Warning: End of video '{video_path}' reached at frame {i + 1}.")
            break

        # Apply static shear effect to the frame
        sheared_frame = apply_static_shear_effect(frame, shear_factor)

        # Write the transformed frame to the output video
        out.write(sheared_frame)

        # Print progress
        print(f"Processed frame {i + 1}/{num_frames_total} for video {video_path}")

    # Release video capture and writer
    cap.release()
    out.release()

def process_videos_in_directory(input_dir, output_dir, shear_factor):
    """
    Apply static shear effect to all videos in the input directory and save the results to the output directory.
    
    Parameters:
        input_dir (str): The path to the input directory containing video files.
        output_dir (str): The path to the output directory to save processed videos.
        shear_factor (float): The shear factor to apply.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith((".mp4",".mov")):  # Adjust this condition based on your file types
            input_video_path = os.path.join(input_dir, filename)
            output_video_path = os.path.join(output_dir, filename)
            
            # Apply static shear effect to the video
            apply_static_shear_effect_to_video(input_video_path, output_video_path, shear_factor)
            print(f"Static shear effect applied to {filename}.")

if __name__ == "__main__":
    input_dir = "C:\\Users\\Wilbert\\Desktop\\data\\cleaned\\assault"
    output_dir = "C:\\Users\\Wilbert\\Desktop\\data\\augmented\\assaultstaticshear"

    # Shear_factor parameter determines the magnitude of the shear effect
    shear_factor = 0.2  # Adjust as needed
    
    # Process all videos in the input directory
    process_videos_in_directory(input_dir, output_dir, shear_factor)

    print("All videos processed successfully.")

