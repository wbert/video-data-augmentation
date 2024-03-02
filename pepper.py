import os
import cv2
import numpy as np
import random

def apply_pepper_effect(frame, pepperness=0.03):
    """
    Apply pepper effect to the frame by randomly adding black pixels.
    
    Parameters:
        frame (numpy.ndarray): The input frame.
        pepperness (float): The probability of adding a black pixel. Default is 0.01.
    
    Returns:
        numpy.ndarray: The frame with pepper effect applied.
    """
    # Create a mask for pepper pixels
    mask = np.random.rand(*frame.shape[:2])
    pepper_pixels = mask < pepperness
    
    # Add black pixels (pepper) to the frame
    frame[pepper_pixels] = 0
    
    return frame

def apply_pepper_effect_to_video(video_path, output_path, pepperness=0.01, num_frames=None):
    """
    Apply pepper effect to each frame of the input video and save the result to a new video.
    
    Parameters:
        video_path (str): The path to the input video file.
        output_path (str): The path to save the output video file.
        pepperness (float): The probability of adding a black pixel. Default is 0.01.
        num_frames (int): The number of frames to process. If None, process all frames. Default is None.
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

        # Apply pepper effect to the frame
        frame_with_pepper = apply_pepper_effect(frame, pepperness=pepperness)

        # Write the transformed frame to the output video
        out.write(frame_with_pepper)

        # Print progress
        print(f"Processed frame {i + 1}/{num_frames_total} for video {video_path}")

    # Release video capture and writer
    cap.release()
    out.release()

def process_videos_in_directory(input_dir, output_dir, pepperness=0.01):
    """
    Apply pepper effect to all videos in the input directory and save the results to the output directory.
    
    Parameters:
        input_dir (str): The path to the input directory containing video files.
        output_dir (str): The path to the output directory to save processed videos.
        pepperness (float): The probability of adding a black pixel. Default is 0.01.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith((".mp4",".mov")):  # Adjust this condition based on your file types
            input_video_path = os.path.join(input_dir, filename)
            output_video_path = os.path.join(output_dir, filename)
            
            # Apply pepper effect to the video
            apply_pepper_effect_to_video(input_video_path, output_video_path, pepperness=pepperness)
            print(f"Pepper effect applied to {filename}.")

if __name__ == "__main__":
    input_dir = "C:\\Users\\Wilbert\\Desktop\\data\\cleaned\\theft"
    output_dir = "C:\\Users\\Wilbert\\Desktop\\data\\augmented\\theftpepper"

    # Pepperness parameter determines the intensity of the effect
    pepperness = 0.01  # Adjust as needed, higher values will result in more pepper
    
    # Process all videos in the input directory
    process_videos_in_directory(input_dir, output_dir, pepperness=pepperness)

    print("All videos processed successfully.")
